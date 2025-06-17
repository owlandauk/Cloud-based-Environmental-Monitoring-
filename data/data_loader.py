"""
Data loading and processing utilities
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Optional

def load_sensor_data(data_provider, room: str, parameter: str) -> Optional[pd.DataFrame]:
    """Load sensor data from the provider and convert to DataFrame"""
    try:
        # Use full data range from CSV files
        start_time = datetime(2024, 9, 24)
        end_time = datetime(2025, 5, 6)
        
        historical_data = data_provider.fetch_sensor_data(room, parameter, start_time, end_time)
        
        if not historical_data:
            return None
        
        # Convert to DataFrame
        df_data = []
        for reading in historical_data:
            df_data.append({
                'timestamp': reading.timestamp,
                'value': reading.value,
                'unit': reading.unit
            })
        
        df = pd.DataFrame(df_data)
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def setup_data_provider():
    """Setup and cache the data provider"""
    if st.session_state.data_provider is None:
        with st.spinner("Loading data..."):
            from data.connector import DataProviderFactory
            st.session_state.data_provider = DataProviderFactory.create_provider()
    
    return st.session_state.data_provider