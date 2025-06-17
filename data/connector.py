"""Data connectors and provider factory"""
from abc import ABC, abstractmethod
from typing import List, Protocol
from datetime import datetime
import streamlit as st

from .models import SensorReading
from .homeassistant_connector import HomeAssistantConnector
from .mock_provider import MockDataProvider
from config.settings import Config

class DataProvider(Protocol):
    """Data provider interface"""
    
    def fetch_sensor_data(self, room: str, parameter: str, 
                         start_time: datetime, end_time: datetime) -> List[SensorReading]:
        ...
    
    def get_available_rooms(self) -> List[str]:
        ...
    
    def get_available_parameters(self, room: str) -> List[str]:
        ...
    
    def is_connected(self) -> bool:
        ...

class DataProviderFactory:
    """Factory for creating appropriate data provider"""
    
    @staticmethod
    def create_provider() -> DataProvider:
        """Create data provider with automatic fallback"""
        
        # Try HomeAssistant connection first
        ha_connector = HomeAssistantConnector(
            Config.HOMEASSISTANT_CONFIG["host"],
            Config.HOMEASSISTANT_CONFIG["port"],
            Config.HOMEASSISTANT_CONFIG["token"]
        )
        
        if ha_connector.test_connection():
            st.success("🔗 Mit HomeAssistant verbunden")
            return ha_connector
        else:
            st.info("📊 Verwende Mock-Daten (HomeAssistant nicht verfügbar)")
            return MockDataProvider()
