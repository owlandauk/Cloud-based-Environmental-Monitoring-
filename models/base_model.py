"""
Base model class that all predictors inherit from
"""

from abc import ABC, abstractmethod
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Tuple

class BasePredictor(ABC):
    """
    Base class for all prediction models
    All models must inherit from this and implement the predict method
    """
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def predict(self, df: pd.DataFrame, cutoff_time: datetime, 
                hours_ahead: int, num_points: int = 20) -> Tuple[List[datetime], List[float]]:
        """
        Generate predictions
        
        Args:
            df: DataFrame with columns ['timestamp', 'value', 'unit']
            cutoff_time: Time from which to start predictions
            hours_ahead: How many hours ahead to predict
            num_points: Number of prediction points to generate
            
        Returns:
            Tuple of (timestamps, predicted_values)
        """
        pass
    
    def _generate_timestamps(self, cutoff_time: datetime, 
                           hours_ahead: int, num_points: int) -> List[datetime]:
        """Helper method to generate prediction timestamps"""
        timestamps = []
        for i in range(1, num_points + 1):
            hours_offset = i * (hours_ahead / num_points)
            timestamp = cutoff_time + timedelta(hours=hours_offset)
            timestamps.append(timestamp)
        return timestamps
    
    def _safe_predict(self, df: pd.DataFrame, cutoff_time: datetime, 
                     hours_ahead: int, num_points: int = 20) -> Tuple[List[datetime], List[float]]:
        """
        Safe wrapper around predict method with error handling
        """
        try:
            return self.predict(df, cutoff_time, hours_ahead, num_points)
        except Exception as e:
            print(f"Error in {self.name}: {e}, using fallback")
            return self._fallback_predict(df, cutoff_time, hours_ahead, num_points)
    
    def _fallback_predict(self, df: pd.DataFrame, cutoff_time: datetime, 
                         hours_ahead: int, num_points: int) -> Tuple[List[datetime], List[float]]:
        """Fallback to constant prediction if model fails"""
        timestamps = self._generate_timestamps(cutoff_time, hours_ahead, num_points)
        last_value = df['value'].iloc[-1]
        values = [last_value] * num_points
        return timestamps, values