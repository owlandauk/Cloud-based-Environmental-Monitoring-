"""
Linear trend predictor - extrapolates based on recent trend
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Tuple
from .base_model import BasePredictor

class LinearTrendPredictor(BasePredictor):
    """
    Predictor that extrapolates based on linear trend from recent data
    """
    
    def __init__(self):
        super().__init__("Linear Trend")
    
    def predict(self, df: pd.DataFrame, cutoff_time: datetime, 
                hours_ahead: int, num_points: int = 20) -> Tuple[List[datetime], List[float]]:
        """
        Predict based on linear trend from recent data points
        """
        
        # Get training data up to cutoff
        training_data = df[df['timestamp'] <= cutoff_time]
        if len(training_data) < 2:
            raise ValueError("Need at least 2 data points for trend analysis")
        
        # Use last 10 points for trend calculation
        recent_data = training_data.tail(10)
        
        # Calculate linear trend
        x = np.arange(len(recent_data))
        y = recent_data['value'].values
        slope, intercept = np.polyfit(x, y, 1)
        
        # Generate timestamps
        timestamps = self._generate_timestamps(cutoff_time, hours_ahead, num_points)
        
        # Generate predictions based on trend
        last_value = training_data['value'].iloc[-1]
        values = []
        
        for i in range(num_points):
            hours_offset = (i + 1) * (hours_ahead / num_points)
            # Apply trend with some damping to avoid unrealistic extrapolation
            trend_value = last_value + (slope * hours_offset * 0.5)
            values.append(trend_value)
        
        return timestamps, values