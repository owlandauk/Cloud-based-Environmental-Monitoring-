"""Data models for the application"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class SensorReading:
    """Represents a single sensor reading"""
    timestamp: datetime
    room: str
    parameter: str
    value: float
    unit: str

@dataclass
class PredictionData:
    """Represents a prediction result"""
    timestamp: datetime
    predicted_value: float
    model_name: str
    confidence: Optional[float] = None
