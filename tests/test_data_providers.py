"""Tests for data providers"""
import pytest
from datetime import datetime, timedelta

from data.mock_provider import MockDataProvider

def test_mock_provider_basic():
    """Test basic mock provider functionality"""
    provider = MockDataProvider()
    
    assert provider.is_connected() == True
    assert len(provider.get_available_rooms()) > 0
    assert len(provider.get_available_parameters("Wohnzimmer")) > 0

def test_mock_data_generation():
    """Test mock data generation"""
    provider = MockDataProvider()
    
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)
    
    data = provider.fetch_sensor_data("Wohnzimmer", "co2", start_time, end_time)
    
    # Will be implemented when mock provider is complete
    # assert len(data) > 0
