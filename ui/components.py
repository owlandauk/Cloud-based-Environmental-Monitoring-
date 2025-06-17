"""Streamlit UI components"""
import streamlit as st
from datetime import datetime

class AppState:
    """Centralized state management"""
    
    @staticmethod
    def initialize():
        """Initialize session state variables"""
        if 'cutoff_time' not in st.session_state:
            st.session_state.cutoff_time = datetime.now()
        if 'data_provider' not in st.session_state:
            st.session_state.data_provider = None
        if 'last_data_fetch' not in st.session_state:
            st.session_state.last_data_fetch = None

class StatusDisplay:
    """Status display components"""
    
    @staticmethod
    def show_metrics(current_value, unit, data_count, prediction_count, connection_status):
        """Display status metrics"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Aktueller Wert", f"{current_value} {unit}")
        with col2:
            st.metric("Datenpunkte", data_count)
        with col3:
            st.metric("Vorhersagen", prediction_count)
        with col4:
            st.metric("Status", connection_status)
