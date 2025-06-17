"""Mock data provider for development - Updated to use real CSV data"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os
import logging
from pathlib import Path

from .models import SensorReading
from config.settings import Config

logger = logging.getLogger(__name__)

class MockDataProvider:
    """Mock data provider using real CSV sensor data"""
    
    def __init__(self):
        self.data_cache: Dict[str, pd.DataFrame] = {}
        self.sensor_mapping = self._create_sensor_mapping()
        self._load_csv_files()
    
    def _create_sensor_mapping(self) -> Dict[str, str]:
        """Map standard parameter names to CSV column names"""
        return {
            "co2": "SCD30_CO2",
            "temperature": "SCD30_Temperature", 
            "humidity": "SCD30_Humidity",
            "pressure": "BME680_Pressure",
            "iaq": "BME680_IAQ",
            "voc": "BME680_Breath_VOC_Equivalent",
            "gas_resistance": "BME680_Gas_Resistance",
            "co": "MICS6814_CO",
            "nh3": "MICS6814_NH3",
            "no2": "MICS6814_NO2"
        }
    
    def _load_csv_files(self):
        """Load all CSV files from the mock_data directory"""
        mock_data_dir = Path(__file__).parent / "mock_data"
        
        if not mock_data_dir.exists():
            logger.warning(f"Mock data directory not found: {mock_data_dir}")
            return
        
        csv_files = list(mock_data_dir.glob("*.csv"))
        logger.info(f"Found {len(csv_files)} CSV files in {mock_data_dir}")
        
        for csv_file in csv_files:
            try:
                # Extract room name from filename (e.g., "Multisensor_104" -> "Sensor 104")
                room_name = self._extract_room_name(csv_file.name)
                
                df = pd.read_csv(csv_file)
                df = self._preprocess_dataframe(df)
                
                self.data_cache[room_name] = df
                logger.info(f"Loaded {len(df)} rows from {csv_file.name} for room '{room_name}'")
                
            except Exception as e:
                logger.error(f"Error loading {csv_file}: {e}")
    
    def _extract_room_name(self, filename: str) -> str:
        """Extract room name from CSV filename"""
        # Remove .csv extension and "combined" suffix
        base_name = filename.replace("_combined.csv", "").replace(".csv", "")
        
        # Convert "Multisensor_104" to "Sensor 104"
        if "Multisensor_" in base_name:
            sensor_id = base_name.replace("Multisensor_", "")
            return f"Sensor {sensor_id}"
        
        # For other naming patterns, just clean up underscores
        return base_name.replace("_", " ").title()
    
    def _preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess the CSV data"""
        # Convert time column to datetime and make timezone-naive
        df['time'] = pd.to_datetime(df['time'])
        if df['time'].dt.tz is not None:
            df['time'] = df['time'].dt.tz_localize(None)
        df = df.sort_values('time')
        
        # Remove rows where time is null
        df = df.dropna(subset=['time'])
        
        # Fill forward numeric columns to handle missing values
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].ffill()
        
        return df
    
    def fetch_sensor_data(self, room: str, parameter: str, 
                         start_time: datetime, end_time: datetime) -> List[SensorReading]:
        """Fetch sensor data from loaded CSV files"""
        
        if room not in self.data_cache:
            logger.warning(f"No data available for room: {room}")
            return self._generate_fallback_data(room, parameter, start_time, end_time)
        
        df = self.data_cache[room]
        
        # Get the CSV column name for this parameter
        csv_column = self.sensor_mapping.get(parameter)
        if csv_column is None or csv_column not in df.columns:
            logger.warning(f"Parameter '{parameter}' (CSV column: {csv_column}) not found in data for room '{room}'")
            logger.warning(f"Available columns: {list(df.columns)}")
            return self._generate_fallback_data(room, parameter, start_time, end_time)
        
        # Debug logging
        logger.info(f"Fetching {parameter} ({csv_column}) for {room}")
        logger.info(f"Time range: {start_time} to {end_time}")
        logger.info(f"DataFrame time range: {df['time'].min()} to {df['time'].max()}")
        
        # Ensure start_time and end_time are timezone-naive like our data
        if start_time.tzinfo is not None:
            start_time = start_time.replace(tzinfo=None)
        if end_time.tzinfo is not None:
            end_time = end_time.replace(tzinfo=None)
        
        # Filter by time range
        mask = (df['time'] >= start_time) & (df['time'] <= end_time)
        filtered_df = df.loc[mask]
        logger.info(f"Rows after time filter: {len(filtered_df)}")
        
        # Check for non-null values in the parameter column
        non_null_mask = filtered_df[csv_column].notna()
        final_df = filtered_df.loc[non_null_mask]
        logger.info(f"Rows with non-null {csv_column}: {len(final_df)}")
        
        # Convert to SensorReading objects
        readings = []
        unit = Config.SENSOR_PARAMETERS.get(parameter, {}).get("unit", "")
        
        for _, row in final_df.iterrows():
            value = row[csv_column]
            readings.append(SensorReading(
                timestamp=row['time'].to_pydatetime(),
                room=room,
                parameter=parameter,
                value=float(value),
                unit=unit
            ))
        
        logger.info(f"Returning {len(readings)} readings for {room}/{parameter}")
        return readings
    
    def _generate_fallback_data(self, room: str, parameter: str, 
                               start_time: datetime, end_time: datetime) -> List[SensorReading]:
        """Generate synthetic data when CSV data is not available"""
        logger.info(f"Generating fallback data for {room}/{parameter}")
        
        # Generate data points every 5 minutes
        current_time = start_time
        readings = []
        unit = Config.SENSOR_PARAMETERS.get(parameter, {}).get("unit", "")
        
        # Base values for different parameters
        base_values = {
            "co2": 400,
            "temperature": 22,
            "humidity": 45,
            "pressure": 1013,
            "iaq": 50,
            "voc": 100
        }
        
        base_value = base_values.get(parameter, 50)
        
        while current_time <= end_time:
            # Simple sine wave with noise for realistic variation
            hours_since_start = (current_time - start_time).total_seconds() / 3600
            daily_cycle = np.sin(2 * np.pi * hours_since_start / 24) * 0.1
            noise = np.random.normal(0, 0.05)
            
            value = base_value * (1 + daily_cycle + noise)
            
            readings.append(SensorReading(
                timestamp=current_time,
                room=room,
                parameter=parameter,
                value=value,
                unit=unit
            ))
            
            current_time += timedelta(minutes=5)
        
        return readings
    
    def get_available_rooms(self) -> List[str]:
        """Get list of available rooms from loaded CSV data"""
        rooms = list(self.data_cache.keys())
        
        # Add fallback rooms if no CSV data is loaded
        if not rooms:
            rooms = Config.ROOMS
        
        return sorted(rooms)
    
    def get_available_parameters(self, room: str) -> List[str]:
        """Get available sensor parameters for a room"""
        if room in self.data_cache:
            df = self.data_cache[room]
            # Find which mapped parameters have data in this CSV
            available = []
            for param, csv_col in self.sensor_mapping.items():
                if csv_col in df.columns and not df[csv_col].isna().all():
                    available.append(param)
            
            # Add any parameters that are configured but not in the mapping
            for param in Config.SENSOR_PARAMETERS.keys():
                if param not in available:
                    available.append(param)
            
            return sorted(available)
        else:
            return list(Config.SENSOR_PARAMETERS.keys())
    
    def is_connected(self) -> bool:
        """Always return True for mock provider"""
        return True
    
    def get_data_summary(self) -> Dict[str, Dict[str, any]]:
        """Get summary information about loaded data"""
        summary = {}
        
        for room, df in self.data_cache.items():
            if not df.empty:
                summary[room] = {
                    "row_count": len(df),
                    "time_range": {
                        "start": df['time'].min().isoformat(),
                        "end": df['time'].max().isoformat()
                    },
                    "available_columns": [col for col in df.columns if col != 'time'],
                    "data_quality": {
                        col: {
                            "non_null_count": df[col].count(),
                            "null_percentage": (df[col].isna().sum() / len(df)) * 100
                        }
                        for col in df.select_dtypes(include=[np.number]).columns
                    }
                }
        
        return summary