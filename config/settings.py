"""
Configuration settings for ML Dashboard - Updated for CSV sensor data
"""
from typing import Dict, List, Any

class Config:
    """Application configuration"""
    
    # Database Configuration
    INFLUX_CONFIG = {
        "host": "localhost",
        "port": 8086,
        "database": "homeassistant"
    }
    
    # HomeAssistant Configuration
    HOMEASSISTANT_CONFIG = {
        "host": "localhost",
        "port": 8123,
        "token": "your_long_lived_access_token_here",
        "timeout": 30
    }
    
    # Application Settings
    APP_CONFIG = {
        "default_history_hours": 24,
        "default_forecast_hours": 6,
        "plot_width": 1200,
        "plot_height": 600,
        "refresh_interval_seconds": 30,
        "cache_ttl_seconds": 300
    }
    
    # Data Configuration - Updated with CSV rooms (will be populated dynamically)
    ROOMS = [
        "Experience Hub",
        "Conference Space"
    ]
    
    # Extended sensor parameters based on CSV data
    SENSOR_PARAMETERS = {
        # Primary environmental sensors
        "co2": {"unit": "ppm", "display_name": "CO2", "color": "#FF6B6B"},
        "temperature": {"unit": "°C", "display_name": "Temperature", "color": "#4ECDC4"},
        "humidity": {"unit": "%", "display_name": "Humidity", "color": "#45B7D1"},
        "pressure": {"unit": "hPa", "display_name": "Pressure", "color": "#96CEB4"},
        
        # Air quality sensors
        "iaq": {"unit": "IAQ", "display_name": "Indoor Air Quality", "color": "#FFEAA7"},
        "voc": {"unit": "VOC", "display_name": "Volatile Organic Compounds", "color": "#DDA0DD"},
        "gas_resistance": {"unit": "Ω", "display_name": "Gas Resistance", "color": "#98D8C8"},
        
        # Gas sensors
        "co": {"unit": "ppm", "display_name": "Carbon Monoxide", "color": "#F7DC6F"},
        "nh3": {"unit": "ppm", "display_name": "Ammonia", "color": "#BB8FCE"},
        "no2": {"unit": "ppm", "display_name": "Nitrogen Dioxide", "color": "#85C1E9"}
    }
    
    # Parameter groups for UI organization
    PARAMETER_GROUPS = {
        "Environmental": ["temperature", "humidity", "pressure"],
        "Air Quality": ["co2", "iaq", "voc"],
        "Gas Detection": ["co", "nh3", "no2", "gas_resistance"]
    }
    
    # Model Configuration
    MODEL_CONFIG = {
        "model_path": "./models/trained/sensor_predictor.joblib",
        "model_type": "sklearn",
        "fallback_model": "simple_trend"
    }
    
    # Logging Configuration
    LOGGING_CONFIG = {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "logs/dashboard.log"
    }
    
    # Data validation thresholds
    DATA_VALIDATION = {
        "co2": {"min": 300, "max": 5000},
        "temperature": {"min": -10, "max": 50},
        "humidity": {"min": 0, "max": 100},
        "pressure": {"min": 900, "max": 1100},
        "iaq": {"min": 0, "max": 500},
        "voc": {"min": 0, "max": 1000},
        "co": {"min": 0, "max": 100},
        "nh3": {"min": 0, "max": 100},
        "no2": {"min": 0, "max": 100}
    }