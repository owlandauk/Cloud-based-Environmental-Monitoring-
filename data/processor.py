"""Data processing utilities"""
import pandas as pd
from typing import List
from .models import SensorReading

class DataProcessor:
    """Data processing and validation utilities"""
    
    @staticmethod
    def readings_to_dataframe(readings: List[SensorReading]) -> pd.DataFrame:
        """Convert sensor readings to pandas DataFrame"""
        if not readings:
            return pd.DataFrame()
        
        data = []
        for reading in readings:
            data.append({
                'timestamp': reading.timestamp,
                'room': reading.room,
                'parameter': reading.parameter,
                'value': reading.value,
                'unit': reading.unit
            })
        
        return pd.DataFrame(data)
    
    @staticmethod
    def validate_data(readings: List[SensorReading]) -> bool:
        """Validate sensor data quality"""
        if not readings:
            return False
        
        # Add validation logic here
        return True
