"""HomeAssistant API connector"""
from typing import List
from datetime import datetime
import requests
import logging

from .models import SensorReading
from config.settings import Config

logger = logging.getLogger(__name__)

class HomeAssistantConnector:
    """Real HomeAssistant API connector"""
    
    def __init__(self, host: str, port: int, token: str):
        self.host = host
        self.port = port
        self.token = token
        self.base_url = f"http://{host}:{port}/api"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def fetch_sensor_data(self, room: str, parameter: str, 
                         start_time: datetime, end_time: datetime) -> List[SensorReading]:
        """Fetch sensor data from HomeAssistant"""
        # TODO: Implement actual API calls
        logger.info(f"Fetching {parameter} data for {room} from {start_time} to {end_time}")
        return []
    
    def get_available_rooms(self) -> List[str]:
        """Get available rooms from HomeAssistant"""
        return Config.ROOMS if self.is_connected() else []
    
    def get_available_parameters(self, room: str) -> List[str]:
        """Get available sensor parameters for room"""
        return list(Config.SENSOR_PARAMETERS.keys()) if self.is_connected() else []
    
    def is_connected(self) -> bool:
        """Check if connected to HomeAssistant"""
        return self.test_connection()
    
    def test_connection(self) -> bool:
        """Test connection to HomeAssistant"""
        try:
            response = requests.get(
                f"{self.base_url}/",
                headers=self.headers,
                timeout=Config.HOMEASSISTANT_CONFIG["timeout"]
            )
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"HomeAssistant connection failed: {e}")
            return False
