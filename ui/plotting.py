"""Plotly plotting utilities"""
import plotly.graph_objects as go
import plotly.express as px
from typing import List
from datetime import datetime
import numpy as np

from data.models import SensorReading, PredictionData
from config.settings import Config

class PlotGenerator:
    """Generate interactive Plotly charts"""
    
    def create_sensor_plot(self, 
                          historical_data: List[SensorReading],
                          predictions: List[PredictionData],
                          cutoff_time: datetime,
                          parameter: str) -> go.Figure:
        """Create interactive timeseries plot with cutoff line"""
        
        fig = go.Figure()
        
        if not historical_data and not predictions:
            fig.add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig
        
        # Get parameter configuration
        param_config = Config.SENSOR_PARAMETERS.get(parameter, {})
        color = param_config.get('color', '#1f77b4')
        unit = param_config.get('unit', '')
        display_name = param_config.get('display_name', parameter.title())
        
        # Split historical data at cutoff
        pre_cutoff_data = [r for r in historical_data if r.timestamp <= cutoff_time]
        post_cutoff_data = [r for r in historical_data if r.timestamp > cutoff_time]
        
        # Plot historical data before cutoff
        if pre_cutoff_data:
            times = [r.timestamp for r in pre_cutoff_data]
            values = [r.value for r in pre_cutoff_data]
            
            fig.add_trace(go.Scatter(
                x=times,
                y=values,
                mode='lines+markers',
                name='Historical Data',
                line=dict(color=color, width=2),
                marker=dict(size=4),
                hovertemplate=f'<b>Historical</b><br>Time: %{{x}}<br>Value: %{{y:.2f}} {unit}<extra></extra>'
            ))
        
        # Plot actual data after cutoff (for validation)
        if post_cutoff_data:
            times = [r.timestamp for r in post_cutoff_data]
            values = [r.value for r in post_cutoff_data]
            
            fig.add_trace(go.Scatter(
                x=times,
                y=values,
                mode='lines+markers',
                name='Actual Data (validation)',
                line=dict(color='orange', width=2),
                marker=dict(size=4),
                hovertemplate=f'<b>Actual</b><br>Time: %{{x}}<br>Value: %{{y:.2f}} {unit}<extra></extra>'
            ))
        
        # Plot predictions
        if predictions:
            pred_times = [p.timestamp for p in predictions]
            pred_values = [p.predicted_value for p in predictions]
            confidences = [p.confidence for p in predictions if p.confidence is not None]
            
            fig.add_trace(go.Scatter(
                x=pred_times,
                y=pred_values,
                mode='lines+markers',
                name='ML Predictions',
                line=dict(color='green', width=2, dash='dash'),
                marker=dict(size=4),
                hovertemplate=f'<b>Prediction</b><br>Time: %{{x}}<br>Value: %{{y:.2f}} {unit}<br>Model: {predictions[0].model_name}<extra></extra>'
            ))
            
            # Add confidence intervals if available
            if confidences and len(confidences) == len(pred_times):
                upper_bound = [v + (1-c) * abs(v) * 0.1 for v, c in zip(pred_values, confidences)]
                lower_bound = [v - (1-c) * abs(v) * 0.1 for v, c in zip(pred_values, confidences)]
                
                fig.add_trace(go.Scatter(
                    x=pred_times + pred_times[::-1],
                    y=upper_bound + lower_bound[::-1],
                    fill='toself',
                    fillcolor='rgba(0,255,0,0.1)',
                    line=dict(color='rgba(255,255,255,0)'),
                    name='Confidence Interval',
                    showlegend=False,
                    hoverinfo='skip'
                ))
        
        # Add cutoff line
        if historical_data or predictions:
            all_values = []
            if historical_data:
                all_values.extend([r.value for r in historical_data])
            if predictions:
                all_values.extend([p.predicted_value for p in predictions])
            
            if all_values:
                y_min = min(all_values) * 0.95
                y_max = max(all_values) * 1.05
                
                fig.add_vline(
                    x=cutoff_time,
                    line=dict(color='red', width=2, dash='dot'),
                    annotation_text="Cutoff Time",
                    annotation_position="top"
                )
        
        # Update layout
        fig.update_layout(
            title=f'{display_name} Over Time',
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
            showlegend=True
        )
        
        return fig
    
    def create_comparison_plot(self, actual_data: List[SensorReading], 
                             predictions: List[PredictionData],
                             parameter: str) -> go.Figure:
        """Create a comparison plot of actual vs predicted values"""
        
        fig = go.Figure()
        
        if not actual_data or not predictions:
            fig.add_annotation(
                text="No data available for comparison",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig
        
        # Get parameter configuration
        param_config = Config.SENSOR_PARAMETERS.get(parameter, {})
        unit = param_config.get('unit', '')
        display_name = param_config.get('display_name', parameter.title())
        
        # Extract values for comparison
        actual_times = [r.timestamp for r in actual_data]
        actual_values = [r.value for r in actual_data]
        pred_times = [p.timestamp for p in predictions]
        pred_values = [p.predicted_value for p in predictions]
        
        # Plot actual values
        fig.add_trace(go.Scatter(
            x=actual_times,
            y=actual_values,
            mode='lines+markers',
            name='Actual',
            line=dict(color='blue', width=2),
            marker=dict(size=6)
        ))
        
        # Plot predicted values
        fig.add_trace(go.Scatter(
            x=pred_times,
            y=pred_values,
            mode='lines+markers',
            name='Predicted',
            line=dict(color='red', width=2, dash='dash'),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title=f'Actual vs Predicted {display_name}',
            xaxis_title='Time',
            yaxis_title=f'{display_name} ({unit})',
            height=400,
            hovermode='x unified'
        )
        
        return fig
    
    def create_error_plot(self, actual_data: List[SensorReading], 
                         predictions: List[PredictionData]) -> go.Figure:
        """Create a plot showing prediction errors over time"""
        
        fig = go.Figure()
        
        if not actual_data or not predictions:
            fig.add_annotation(
                text="No data available for error analysis",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig
        
        # Calculate errors by finding closest predictions to actual data points
        errors = []
        error_times = []
        
        for actual in actual_data:
            # Find closest prediction
            closest_pred = min(predictions, 
                             key=lambda p: abs((p.timestamp - actual.timestamp).total_seconds()))
            
            # Only include if within reasonable time window (e.g., 30 minutes)
            time_diff = abs((closest_pred.timestamp - actual.timestamp).total_seconds())
            if time_diff <= 1800:  # 30 minutes
                error = abs(actual.value - closest_pred.predicted_value)
                errors.append(error)
                error_times.append(actual.timestamp)
        
        if errors:
            fig.add_trace(go.Scatter(
                x=error_times,
                y=errors,
                mode='lines+markers',
                name='Prediction Error',
                line=dict(color='red', width=2),
                marker=dict(size=6),
                hovertemplate='<b>Error</b><br>Time: %{x}<br>Error: %{y:.2f}<extra></extra>'
            ))
            
            # Add average error line
            avg_error = np.mean(errors)
            fig.add_hline(
                y=avg_error,
                line=dict(color='orange', width=2, dash='dash'),
                annotation_text=f"Avg Error: {avg_error:.2f}"
            )
        
        fig.update_layout(
            title='Prediction Error Over Time',
            xaxis_title='Time',
            yaxis_title='Absolute Error',
            height=400,
            hovermode='x unified'
        )
        
        return fig