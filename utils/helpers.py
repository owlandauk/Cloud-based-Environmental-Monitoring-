"""Helper utilities"""
import logging
import os
from datetime import datetime
from config.settings import Config

def setup_logging():
    """Setup application logging"""
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, Config.LOGGING_CONFIG["level"]),
        format=Config.LOGGING_CONFIG["format"],
        handlers=[
            logging.FileHandler(Config.LOGGING_CONFIG["file"]),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Logging setup complete")

def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp for display"""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def validate_time_range(start_time: datetime, end_time: datetime) -> bool:
    """Validate time range parameters"""
    return start_time < end_time and end_time <= datetime.now()
