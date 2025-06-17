# 🏠 Sensor Forecast Dashboard

A local web dashboard for visualizing and validating ML models for air sensor predictions based on HomeAssistant data.

![Dashboard Preview](docs/dashboard-preview.png)

## 🎯 Overview

The Sensor Forecast Dashboard enables visualization and validation of ML predictions for environmental sensors (CO2, temperature, humidity, etc.). Through a movable cutoff point, you can create "What-If" scenarios and analyze model performance.

### ✨ Key Features

- 📊 **Interactive time series visualization** with 24h history
- 🤖 **ML predictions** for the next 6 hours
- ⚡ **Movable cutoff point** for flexible validation
- 🔄 **Automatic fallback** to mock data when HomeAssistant is unavailable
- 📱 **Responsive design** optimized for presentations
- 🎛️ **Multi-room support** with sensor-specific parameters

## 🚀 Quick Start

### 1. Installation

```bash
# Create virtual environment (REQUIRED)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**⚠️ Important:** Always activate the virtual environment before running the dashboard!

### 2. Configuration

Create a `.env` file or edit `config/settings.py`:

```python
# HomeAssistant Configuration
HOMEASSISTANT_CONFIG = {
    "host": "192.168.1.100",  # Your HomeAssistant IP
    "port": 8123,
    "token": "eyJ0eXAiOiJKV1Q...",  # Long-Lived Access Token
    "timeout": 30
}
```

### 3. Launch

```bash
# Make sure virtual environment is activated (you should see (venv) in your prompt)
# If not activated:
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

streamlit run main.py
```

Dashboard opens automatically at: **http://localhost:8501**

### 4. VS Code Setup (Recommended)

If using VS Code:

1. **Select Python Interpreter:**

   - Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
   - Type "Python: Select Interpreter"
   - Choose: `./venv/bin/python` (macOS/Linux) or `./venv/Scripts/python.exe` (Windows)

2. **Create `.vscode/settings.json`:**
   ```json
   {
     "python.defaultInterpreterPath": "./venv/bin/python",
     "python.terminal.activateEnvironment": true,
     "python.linting.enabled": true,
     "python.linting.flake8Enabled": true,
     "python.formatting.provider": "black"
   }
   ```

## 📁 Project Structure

```
sensor-forecast-dashboard/
├── 📄 main.py                          # Streamlit Entry Point
├── 📄 requirements.txt                 # Python Dependencies
├── 📄 README.md                       # This file
├── 📄 .env.example                    # Example configuration
├── 📂 config/
│   ├── 📄 settings.py                 # Central configuration
│   └── 📄 __init__.py
├── 📂 data/
│   ├── 📄 connector.py                # Data Provider Factory
│   ├── 📄 homeassistant_connector.py  # HomeAssistant API Integration
│   ├── 📄 mock_provider.py            # Mock data for development
│   ├── 📄 processor.py                # Data processing
│   ├── 📄 models.py                   # Data models (SensorReading, etc.)
│   └── 📄 __init__.py
├── 📂 models/
│   ├── 📄 predictor.py                # ML Model Wrapper
│   ├── 📂 trained/                    # Trained model files (.pkl/.joblib)
│   │   └── 📄 .gitkeep
│   └── 📄 __init__.py
├── 📂 ui/
│   ├── 📄 components.py               # Streamlit UI Components
│   ├── 📄 plotting.py                 # Plotly Visualizations
│   └── 📄 __init__.py
├── 📂 utils/
│   ├── 📄 helpers.py                  # Utility Functions
│   └── 📄 __init__.py
├── 📂 tests/
│   ├── 📄 test_data_providers.py      # Unit Tests
│   └── 📄 __init__.py
├── 📂 docs/                           # Documentation
└── 📂 logs/                           # Application Logs
    └── 📄 .gitkeep
```

## ⚙️ Configuration

### HomeAssistant Setup

1. **Create Long-Lived Access Token:**

   - In HomeAssistant: Profile → Security → Long-Lived Access Tokens
   - Create token and copy

2. **Configure sensors:**

   ```python
   # In config/settings.py
   SENSOR_PARAMETERS = {
       "co2": {"unit": "ppm", "display_name": "CO2"},
       "temperature": {"unit": "°C", "display_name": "Temperature"},
       "humidity": {"unit": "%", "display_name": "Humidity"},
       "pressure": {"unit": "hPa", "display_name": "Pressure"}
   }
   ```

3. **Define rooms:**
   ```python
   ROOMS = [
       "Living Room",
       "Bedroom",
       "Kitchen",
       "Office"
   ]
   ```

### Mock Data Mode

When HomeAssistant is unavailable, the system automatically uses realistic mock data featuring:

- ✅ Natural daily cycles
- ✅ Room-specific differences
- ✅ Realistic sensor fluctuations
- ✅ Various environmental parameters

## 🤖 ML Models

### Default Model (Simple Trend)

The integrated fallback model uses:

- Trend-based extrapolation
- Time-of-day consideration
- Dampened predictions over time
- Realistic noise component

### Adding Custom Models

```python
# Save trained scikit-learn model
import joblib
joblib.dump(your_model, 'models/trained/sensor_predictor.joblib')

# Dashboard loads it automatically
```

**Supported formats:**

- scikit-learn (.joblib/.pkl)
- Additional frameworks planned

## 🎮 Usage

### 1. Open Dashboard

```bash
streamlit run main.py
```

### 2. Select Parameters

- **Room** from available rooms
- **Sensor** (CO2, temperature, etc.)
- **Cutoff time** for prediction start

### 3. Perform Analysis

- **Blue line:** Historical real data
- **Red dashed line:** Cutoff point (adjustable)
- **Green line:** ML predictions
- **Gray background:** Past
- **White background:** Future

### 4. Validation

- Set cutoff in the past
- Compare predictions with actual values
- Evaluate model performance

## 📊 Visualization

The dashboard offers:

### Interactive Plots

- **Zoom & Pan:** Detailed view of different time ranges
- **Hover Info:** Exact values and timestamps
- **Responsive Design:** Automatic screen size adaptation

### Status Metrics

- **Current Value:** Latest sensor reading
- **Data Points:** Number of historical values
- **Predictions:** Number of generated forecasts
- **Connection Status:** HomeAssistant/Mock mode

## 🔧 Development

### Development Environment

```bash
# Always start by activating virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Verify you're in the virtual environment (should see (venv) in prompt)

# Install development dependencies (if you haven't already)
pip install -r requirements.txt

# Run tests
pytest tests/

# Format code
black .
flake8 .
```

**💡 Pro Tip:** Create a script to activate venv automatically:

**Windows (`activate.bat`):**

```batch
@echo off
call venv\Scripts\activate
echo Virtual environment activated!
```

**macOS/Linux (`activate.sh`):**

```bash
#!/bin/bash
source venv/bin/activate
echo "Virtual environment activated!"
```

### Adding New Features

The modular design enables easy extensions:

1. **New Data Sources:** Implement the `DataProvider` interface
2. **ML Models:** Extend the `ModelPredictor` class
3. **Visualizations:** New plots in `PlotGenerator`
4. **UI Components:** Additional Streamlit components

### Testing

```bash
# Run all tests
pytest tests/

# With coverage
pytest tests/ --cov=. --cov-report=html

# Specific tests
pytest tests/test_data_providers.py -v
```

## 🚀 Deployment

### Local Network

```bash
# Activate virtual environment first!
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# For access from other devices
streamlit run main.py --server.address 0.0.0.0 --server.port 8501
```

### Docker (optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.address", "0.0.0.0"]
```

## 📈 Performance

### Optimizations

- **Caching:** 5-minute cache for database queries
- **Lazy Loading:** Models loaded only when needed
- **Efficient Rendering:** Streamlit-optimized components

### Resource Usage

- **RAM:** < 512MB under normal usage
- **CPU:** Low, except during ML computations
- **Network:** Minimal for local usage

## 🐛 Troubleshooting

### Common Issues

**Virtual environment not activated:**

```bash
# You should see (venv) in your terminal prompt
# If not, activate it:
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
```

**"Command not found" errors:**

```bash
# Make sure virtual environment is activated first
# Then reinstall if needed:
pip install -r requirements.txt
```

**HomeAssistant connection failed:**

```bash
# Check logs
tail -f logs/dashboard.log

# Test network connectivity
curl http://YOUR_HA_IP:8123/api/
```

**Streamlit won't start:**

```bash
# Port already in use
streamlit run main.py --server.port 8502

# Missing dependencies (make sure venv is activated)
pip install -r requirements.txt
```

**VS Code Python interpreter issues:**

1. Open Command Palette (`Ctrl+Shift+P`)
2. "Python: Select Interpreter"
3. Choose the venv interpreter: `./venv/bin/python` or `./venv/Scripts/python.exe`

**No data available:**

- Mock data is used automatically
- Check HomeAssistant token and IP
- Check logs for detailed error messages

### Debug Mode

```python
# In config/settings.py
LOGGING_CONFIG = {
    "level": "DEBUG",  # Instead of "INFO"
    # ...
}
```

## 🛣️ Roadmap

### Version 1.1 (Planned)

- [ ] **Live Updates:** Automatic data refresh
- [ ] **Confidence Intervals:** Prediction uncertainty visualization
- [ ] **Multi-Sensor Comparison:** Multiple parameters simultaneously
- [ ] **Export Functions:** CSV/PNG export

### Version 1.2 (Future)

- [ ] **Advanced ML Models:** LSTM, Prophet integration
- [ ] **Alert System:** Threshold notifications
- [ ] **Historical Analysis:** Long-term trend analysis
- [ ] **API Interface:** REST API for external integration

### Version 2.0 (Vision)

- [ ] **Multi-Home Support:** Multiple HomeAssistant instances
- [ ] **Cloud Deployment:** Optional cloud-based variant
- [ ] **Mobile App:** Companion smartphone app
- [ ] **Advanced Analytics:** Correlation analysis, anomaly detection

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Create Pull Request

### Code Standards

- **Python Style:** PEP 8 with Black formatting
- **Documentation:** Docstrings for all public functions
- **Tests:** Minimum 80% code coverage
- **Type Hints:** Complete type annotations

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit** for the excellent dashboard framework
- **Plotly** for interactive visualizations
- **HomeAssistant** community for sensor integration
- **scikit-learn** for ML functionality

## 📞 Support

For questions or issues:

- 📧 **Issues:** GitHub Issues for bug reports and feature requests
- 📚 **Documentation:** Additional details in `docs/` folder
- 💬 **Discussions:** GitHub Discussions for general questions

---

**Happy Forecasting! 🚀📊**
