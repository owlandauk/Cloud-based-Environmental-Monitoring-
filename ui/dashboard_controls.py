"""
Dashboard UI controls and components
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Tuple, Optional
from config.settings import Config
from models.model_factory import get_available_models

def create_top_controls(data_provider) -> Tuple[str, str, str, int]:
    """Create the top control bar with room, parameter, predictor, and forecast selection"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Room selection
        available_rooms = data_provider.get_available_rooms()
        if not available_rooms:
            st.error("No rooms available")
            return None, None, None, None
            
        if st.session_state.selected_room not in available_rooms:
            st.session_state.selected_room = available_rooms[0]
        
        selected_room = st.selectbox(
            "🏠 Room",
            available_rooms,
            index=available_rooms.index(st.session_state.selected_room)
        )
        st.session_state.selected_room = selected_room
    
    with col2:
        # Parameter selection
        available_parameters = data_provider.get_available_parameters(selected_room)
        if not available_parameters:
            st.error("No parameters available")
            return selected_room, None, None, None
            
        if st.session_state.selected_parameter not in available_parameters:
            st.session_state.selected_parameter = available_parameters[0]
        
        selected_parameter = st.selectbox(
            "📊 Parameter",
            available_parameters,
            index=available_parameters.index(st.session_state.selected_parameter),
            format_func=lambda x: Config.SENSOR_PARAMETERS.get(x, {}).get('display_name', x.title())
        )
        st.session_state.selected_parameter = selected_parameter
    
    with col3:
        # Predictor selection
        available_models = get_available_models()
        selected_predictor = st.selectbox(
            "🤖 Predictor",
            available_models,
            index=available_models.index(st.session_state.predictor_type) if st.session_state.predictor_type in available_models else 0
        )
        st.session_state.predictor_type = selected_predictor
    
    with col4:
        # Forecast hours
        forecast_hours = st.selectbox(
            "⏰ Forecast Hours",
            [1, 3, 6, 12, 24],
            index=2  # Default to 6 hours
        )
    
    return selected_room, selected_parameter, selected_predictor, forecast_hours

def create_analysis_window_controls(df: pd.DataFrame) -> pd.DataFrame:
    """Create compact analysis window controls and return filtered dataframe"""
    
    # Compact single-line control
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        # Simple lookback window in hours
        lookback_hours = st.selectbox(
            "📊 Lookback Window",
            [1, 3, 6, 12, 24, 48, 72],
            index=4,  # Default to 24 hours
            help="How many hours of recent data to analyze"
        )
    
    with col2:
        # Show the actual time range being analyzed
        data_end = df['timestamp'].max()
        analysis_start = data_end - timedelta(hours=lookback_hours)
        st.info(f"📅 {analysis_start.strftime('%m-%d %H:%M')} to {data_end.strftime('%m-%d %H:%M')}")
    
    with col3:
        # Show data point count
        df_windowed = df[df['timestamp'] >= analysis_start]
        st.metric("Points", len(df_windowed))
    
    return df_windowed

def create_cutoff_control(chart_start_time, chart_end_time) -> float:
    """
    Create cutoff control slider that aligns with chart timeline
    Returns cutoff as a fraction (0.0 to 1.0) of the chart timeline
    """
    # Calculate the total time span of the chart
    total_duration = (chart_end_time - chart_start_time).total_seconds() / 3600  # in hours
    
    # Create slider that represents position along the chart timeline
    cutoff_position = st.slider(
        "",  # No label
        min_value=0.1,  # 10% through the data
        max_value=1.0,  # 100% = at the end of the data
        value=0.7,      # Default 70% through
        step=0.01,      # Fine control
        format="%.0f%%",  # Show as percentage
        help="Position of cutoff line - drag to adjust where training ends",
        key="cutoff_position"
    )
    
    return cutoff_position

def create_metrics_display(df: pd.DataFrame, cutoff_position: float, forecast_hours: int):
    """Create the metrics display below the chart"""
    cutoff_index = int(len(df) * cutoff_position)
    training_count = cutoff_index
    validation_count = len(df) - cutoff_index
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Training Points", training_count)
    with col2:
        st.metric("Validation Points", validation_count)
    with col3:
        st.metric("Forecast Hours", forecast_hours)

def initialize_session_state():
    """Initialize all session state variables"""
    if 'data_provider' not in st.session_state:
        st.session_state.data_provider = None
    if 'selected_room' not in st.session_state:
        st.session_state.selected_room = None
    if 'selected_parameter' not in st.session_state:
        st.session_state.selected_parameter = None
    if 'predictor_type' not in st.session_state:
        st.session_state.predictor_type = "Constant Value"