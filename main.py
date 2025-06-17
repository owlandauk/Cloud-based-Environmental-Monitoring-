"""
ML Sensor Forecast Dashboard - Main Application
Clean, modular implementation
"""

import streamlit as st
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules with correct paths
from utils.helpers import setup_logging
from ui.dashboard_controls import (
    initialize_session_state, 
    create_top_controls, 
    create_analysis_window_controls,
    create_cutoff_control,
    create_metrics_display
)
from data.data_loader import setup_data_provider, load_sensor_data
from ui.chart_components import create_sensor_chart

def main():
    """Main application entry point"""
    
    # Basic setup
    setup_logging()
    st.set_page_config(
        page_title="ML Sensor Dashboard",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("🏠 ML Sensor Forecast Dashboard")
    
    # Setup data provider
    data_provider = setup_data_provider()
    if not data_provider:
        st.error("Failed to setup data provider")
        return
    
    # Top controls
    selected_room, selected_parameter, selected_predictor, forecast_hours = create_top_controls(data_provider)
    
    if not selected_room or not selected_parameter:
        st.info("👆 Please select a room and parameter to view data")
        return
    
    # Load data
    df = load_sensor_data(data_provider, selected_room, selected_parameter)
    
    if df is None or df.empty:
        st.error("No data available for the selected room and parameter")
        return
    
    # Compact analysis window controls (single line)
    df_windowed = create_analysis_window_controls(df)
    
    if df_windowed.empty:
        st.error("No data in the selected time window")
        return
    
    # Get chart time range for slider alignment
    chart_start_time = df_windowed['timestamp'].min()
    chart_end_time = df_windowed['timestamp'].max()
    
    # Create and display chart with cutoff control
    try:
        # Use session state to track cutoff position
        if 'cutoff_position' not in st.session_state:
            st.session_state.cutoff_position = 0.7
        
        # Create chart with current cutoff position
        fig = create_sensor_chart(
            df_windowed, 
            st.session_state.cutoff_position, 
            selected_predictor, 
            forecast_hours, 
            selected_parameter,
            selected_room
        )
        
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Cutoff control slider BELOW the chart (aligned with chart timeline)
        cutoff_position = create_cutoff_control(chart_start_time, chart_end_time)
        
        # Update session state and recreate chart if slider moved
        if abs(cutoff_position - st.session_state.cutoff_position) > 0.01:
            st.session_state.cutoff_position = cutoff_position
            st.rerun()  # Rerun to update the chart
        
        # Metrics display
        create_metrics_display(df_windowed, cutoff_position, forecast_hours)
        
    except Exception as e:
        st.error(f"Error creating chart: {e}")
        with st.expander("🐛 Debug Info"):
            st.exception(e)

if __name__ == "__main__":
    main()