import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Tuple
from .base_model import BasePredictor
import joblib


class XGBoostMultiOutputPredictor(BasePredictor):
    """
    XGBoost Multi-Output Predictor
    Predicts a selected sensor variable using a trained XGBoost model
    """

    def __init__(self):
        super().__init__("XGBoost Multi-Output Predictor")
        self.model = joblib.load('models/trained/xgboost_best_mode.pkl')

        # Mapping from dashboard parameter to internal column name
        self.param_map = {
            "Temperature": "currentEnvironmentTemperature",
            "Humidity": "humidityLevel",
            "CO2": "carbonDioxidePPM",
            "Pressure": "airPressure",
            "Illuminance": "currentIlluminance"
        }

    def predict(self, df: pd.DataFrame, cutoff_time: datetime,
                hours_ahead: int, num_points: int = 20, parameter: str = "Temperature") -> Tuple[List[datetime], List[float]]:

        # Validate parameter and get target column
        target_col = self.param_map.get(parameter)
        if not target_col:
            raise ValueError(f"Unsupported parameter: {parameter}")

        # Columns used for model input
        target_columns = list(self.param_map.values())

        # 1. Time series preparation
        df = df.set_index('timestamp').sort_index()
        df = df[target_columns].resample('5min').mean()
        df = df.interpolate(method='time')

        # 2. Add cyclical time features
        df = self.engineer_features(df)

        # 3. Select history before cutoff
        history = df[df.index <= cutoff_time]
        if history.empty:
            raise ValueError("No data available before cutoff_time")

        # 4. Create time-aware prediction input
        last_row = history.iloc[-1]
        sensor_values = last_row[target_columns].values
        future_timestamps = self._generate_timestamps(cutoff_time, hours_ahead, num_points)
        X_pred = pd.DataFrame([sensor_values] * num_points, columns=target_columns)
        X_pred.index = future_timestamps
        X_pred = self.engineer_features(X_pred)

        # 5. Model prediction
        y_pred = self.model.predict(X_pred)

        # 6. Return only selected variable
        idx = target_columns.index(target_col)
        return future_timestamps, y_pred[:, idx].tolist()

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df = df.sort_index()  # Ensure time order
        df['minute'] = df.index.minute
        df['hour'] = df.index.hour
        df['day_of_week'] = df.index.dayofweek
        df['month'] = df.index.month

        df['minute_sin'] = np.sin(2 * np.pi * df['minute'] / 60)
        df['minute_cos'] = np.cos(2 * np.pi * df['minute'] / 60)
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)

        return df.drop(columns=['minute', 'hour', 'day_of_week', 'month'])

    def _generate_timestamps(self, start_time: datetime, hours_ahead: int, num_points: int) -> List[datetime]:
        interval_minutes = (hours_ahead * 60) // num_points
        return [start_time + pd.Timedelta(minutes=interval_minutes * (i + 1)) for i in range(num_points)]

