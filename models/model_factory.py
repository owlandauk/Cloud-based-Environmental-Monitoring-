"""
Model factory - registers and manages all prediction models
This is the ONLY file that needs to be updated when adding new models
"""

from typing import Dict, List, Tuple
import pandas as pd
from datetime import datetime

# Import all model classes
from .constant_predictor import ConstantPredictor
from .linear_trend_predictor import LinearTrendPredictor

# Import teammate models (add new imports here as teammates create models)
# from .lstm_predictor import LSTMPredictor
# from .random_forest_predictor import RandomForestPredictor
# from .transformer_predictor import TransformerPredictor
from .xgboost_multi_output_predictor import XGBoostMultiOutputPredictor
class ModelFactory:

    """
    Factory for creating and managing prediction models
    
    To add a new model:
    1. Create your model file (e.g., lstm_predictor.py)
    2. Import it at the top of this file
    3. Add it to the _models dictionary below
    4. That's it! It will appear in the dashboard dropdown
    """
    
    def __init__(self):
        # Register all available models here
        # Format: "Display Name": ModelClass
        self._models = {
            "Constant Value": ConstantPredictor,
            "Linear Trend": LinearTrendPredictor,
            
            # Add teammate models here:
            # "LSTM Neural Network": LSTMPredictor,
            # "Random Forest": RandomForestPredictor,
            # "Transformer": TransformerPredictor,
            "XGBoost Multi-Output Predictor": XGBoostMultiOutputPredictor,
        }
        
        # Cache instantiated models for performance
        self._model_instances = {}
    
    def get_available_models(self) -> List[str]:
        """Get list of available model names for the dropdown"""
        return list(self._models.keys())
    
    def get_model(self, model_name: str):
        """Get a model instance (cached for performance)"""
        if model_name not in self._models:
            raise ValueError(f"Unknown model: {model_name}")
        
        # Use cached instance if available
        if model_name not in self._model_instances:
            model_class = self._models[model_name]
            self._model_instances[model_name] = model_class()
        
        return self._model_instances[model_name]
    
    def predict(self, model_name: str, df: pd.DataFrame, cutoff_time: datetime, 
                hours_ahead: int, num_points: int = 20) -> Tuple[List[datetime], List[float]]:
        """
        Generate predictions using the specified model
        
        Args:
            model_name: Name of the model to use
            df: DataFrame with sensor data
            cutoff_time: Time to start predictions from
            hours_ahead: How many hours to predict ahead
            num_points: Number of prediction points
            
        Returns:
            (timestamps, predicted_values)
        """
        model = self.get_model(model_name)
        return model._safe_predict(df, cutoff_time, hours_ahead, num_points)

# Global factory instance
model_factory = ModelFactory()

# Convenience functions for the dashboard
def get_available_models() -> List[str]:
    """Get list of available model names"""
    return model_factory.get_available_models()

def generate_predictions(model_name: str, df: pd.DataFrame, cutoff_time: datetime, 
                        hours_ahead: int, num_points: int = 20) -> Tuple[List[datetime], List[float]]:
    """Generate predictions using the specified model"""
    return model_factory.predict(model_name, df, cutoff_time, hours_ahead, num_points)

# Instructions for teammates:
"""
To add your model to the dashboard:

1. Create your model file: models/your_model_name.py
   - Use the template in teammate_model_template.py
   - Inherit from BasePredictor
   - Implement the predict() method

2. Add import at the top of THIS file:
   from .your_model_name import YourModelClass

3. Add to the _models dictionary:
   "Your Model Display Name": YourModelClass,

Example:
   from .lstm_predictor import LSTMPredictor
   
   self._models = {
       "Constant Value": ConstantPredictor,
       "Linear Trend": LinearTrendPredictor,
       "LSTM Neural Network": LSTMPredictor,  # ← Add this line
   }

That's it! Your model will appear in the dropdown automatically.
"""
