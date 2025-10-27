🌦️ Modern Weather App — Streamlit

    A real-time weather dashboard built using Python, Streamlit, and Plotly, powered by the OpenWeatherMap API.It display current weather conditions and a 5-day forecast with a morden animater interface.

Features
    - 🌍 Live current weather  
    - 📈 5-day forecast chart  
    - 🌡 Unit toggle (°C ↔ °F)  
    - 🕓 Auto-refresh every 1 min  
    - 🌤 Animated weather backgrounds

Technologies Used
    - Python 3.10
    - Streamlit-Web app framework
    - Requests-API integration
    - Plotly Express-Data visualization
    - Pandas-Data handling
    - OpenWeatherMap API  

Setup
  bash
    Clone the repo
      git clone https://github.com/yourusername/weather-app.git
      cd weather-app

    Install dependencies
      pip install -r requirements.txt
      pip install streamlit requests pandas plotly streamlit-autorefersh

    Run the app
      streamlit run weather_forecast_app.py

API Key
    Creat a free account on OpenWeatherMap
    copy your API key and replace it in the code:
      API_KEY = "your_api_key_here"

Project Structure
  Weather-App
    weather_app.py
    weather_forecast_app.py
    weather_test.py
    README.md
    requirements.txt