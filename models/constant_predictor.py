"""
Constant value predictor - always predicts the last known value
"""

import pandas as pd
from datetime import datetime
from typing import List, Tuple
from .base_model import BasePredictor

class ConstantPredictor(BasePredictor):
    """
    Simple predictor that always predicts the last known value
    Good for testing and as a baseline
    """
    
    def __init__(self):
        super().__init__("Constant Value")
    
    def predict(self, df: pd.DataFrame, cutoff_time: datetime, 
                hours_ahead: int, num_points: int = 20) -> Tuple[List[datetime], List[float]]:
        """
        Predict constant value based on last known data point
        """
        
        # Get the last value from the training data (up to cutoff_time)
        training_data = df[df['timestamp'] <= cutoff_time]
        if training_data.empty:
            raise ValueError("No training data available")
        
        last_value = training_data['value'].iloc[-1]
        
        # Generate timestamps
        timestamps = self._generate_timestamps(cutoff_time, hours_ahead, num_points)
        
        # Generate constant predictions
        values = [last_value] * num_points
        
        return timestamps, values