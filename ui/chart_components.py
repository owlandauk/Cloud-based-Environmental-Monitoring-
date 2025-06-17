"""
Chart creation components for the sensor dashboard
"""

import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from config.settings import Config
from models.model_factory import generate_predictions

def create_sensor_chart(df: pd.DataFrame, cutoff_position: float, predictor_type: str, 
                       forecast_hours: int, parameter: str, room: str) -> go.Figure:
    """Create the main sensor data chart with predictions"""
    
    if df is None or df.empty:
        return create_empty_chart("No data to display")
    
    # Get parameter configuration
    param_config = Config.SENSOR_PARAMETERS.get(parameter, {})
    unit = param_config.get('unit', '')
    display_name = param_config.get('display_name', parameter.title())
    
    # Calculate cutoff point based on position (0.0 to 1.0)
    cutoff_index = int(len(df) * cutoff_position)
    cutoff_time = df.iloc[cutoff_index]['timestamp']
    
    # Ensure cutoff_time is a proper datetime object
    if hasattr(cutoff_time, 'to_pydatetime'):
        cutoff_time = cutoff_time.to_pydatetime()
    
    # Split data
    training_df = df.iloc[:cutoff_index]
    validation_df = df.iloc[cutoff_index:]
    
    # Generate predictions using the new model factory
    pred_times, pred_values = [], []
    if not training_df.empty:
        try:
            pred_times, pred_values = generate_predictions(
                predictor_type, df, cutoff_time, forecast_hours, num_points=20
            )
        except Exception as e:
            print(f"Prediction error: {e}")
    
    # Determine chart end time (end of predictions)
    chart_end_time = pred_times[-1] if pred_times else cutoff_time
    
    # Limit validation data to only show up to the end of predictions
    if not validation_df.empty:
        validation_df = validation_df[validation_df['timestamp'] <= chart_end_time]
    
    # Create figure
    fig = go.Figure()
    
    # Add training data trace
    if not training_df.empty:
        fig.add_trace(go.Scatter(
            x=training_df['timestamp'],
            y=training_df['value'],
            mode='lines',
            name='Training Data',
            line=dict(color='#1f77b4', width=2),
            hovertemplate=f'<b>Training</b><br>Time: %{{x}}<br>Value: %{{y:.2f}} {unit}<extra></extra>'
        ))
    
    # Add validation data trace
    if not validation_df.empty:
        fig.add_trace(go.Scatter(
            x=validation_df['timestamp'],
            y=validation_df['value'],
            mode='lines',
            name='Actual Data',
            line=dict(color='#ff7f0e', width=2),
            hovertemplate=f'<b>Actual</b><br>Time: %{{x}}<br>Value: %{{y:.2f}} {unit}<extra></extra>'
        ))
    
    # Add predictions trace
    if pred_times and pred_values:
        fig.add_trace(go.Scatter(
            x=pred_times,
            y=pred_values,
            mode='lines+markers',
            name=f'Predictions ({predictor_type})',
            line=dict(color='#2ca02c', width=2, dash='dash'),
            marker=dict(size=4),
            hovertemplate=f'<b>Prediction</b><br>Time: %{{x}}<br>Value: %{{y:.2f}} {unit}<extra></extra>'
        ))
    
    # Add cutoff line
    add_cutoff_line(fig, cutoff_time)
    
    # Update layout
    fig.update_layout(
        title=f'{display_name} - {room}',
        xaxis_title='Time',
        yaxis_title=f'{display_name} ({unit})',
        height=600,
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        margin=dict(t=50, b=10)  # Minimal bottom margin
    )
    
    return fig

def add_cutoff_line(fig: go.Figure, cutoff_time: datetime):
    """Add cutoff line and annotation to the chart"""
    fig.add_shape(
        type="line",
        x0=cutoff_time,
        x1=cutoff_time,
        y0=0,
        y1=1,
        yref="paper",
        line=dict(color="red", width=2, dash="dot"),
    )
    
    fig.add_annotation(
        x=cutoff_time,
        y=1,
        yref="paper",
        text="Cutoff",
        showarrow=False,
        yshift=10,
        bgcolor="white",
        bordercolor="red",
        borderwidth=1
    )

def create_empty_chart(message: str) -> go.Figure:
    """Create an empty chart with a message"""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5, 
        showarrow=False,
        font=dict(size=16)
    )
    fig.update_layout(
        height=400,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig