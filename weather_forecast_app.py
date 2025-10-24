import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ==============================
# Auto-refresh every 1 min
# ==============================
st_autorefresh(interval=60*1000, key="auto_refresh")

# ==============================
# API Setup
# ==============================
API_KEY = "a97fd12f6837909eb8dcb30ef64f7c64"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# ==============================
# Page Config
# ==============================
st.set_page_config(page_title="Modern Weather App", page_icon="🌦️", layout="wide")
st.title("🌍 Modern Real-Time Weather & 5-Day Forecast")

# ==============================
# Unit Toggle
# ==============================
unit = st.radio("Select Units", ("Celsius (°C)", "Fahrenheit (°F)"), horizontal=True)
units_param = "metric" if unit.startswith("C") else "imperial"

# ==============================
# City Input
# ==============================
city_input = st.text_input("🏙️ Enter City Name (e.g., London,GB):")
st.markdown("**Quick Sample Cities:**")
cols = st.columns(4)
sample_cities = ["Paris,FR", "London,GB", "Delhi,IN", "New York,US"]
for col, city in zip(cols, sample_cities):
    if col.button(city):
        city_input = city

# ==============================
# Helper Functions
# ==============================
def get_icon(weather_desc, is_day=True):
    weather_desc = weather_desc.lower()
    if "cloud" in weather_desc: return "☁️"
    if "rain" in weather_desc: return "🌧️"
    if "clear" in weather_desc: return "☀️" if is_day else "🌙"
    if "snow" in weather_desc: return "❄️"
    if "thunder" in weather_desc: return "⛈️"
    if "mist" in weather_desc or "fog" in weather_desc: return "🌫️"
    return "🌈"

def fetch_weather(city):
    params = {"q": city, "appid": API_KEY, "units": units_param}
    response = requests.get(BASE_URL, params=params)
    return response.json(), response.status_code

def fetch_forecast(city):
    params = {"q": city, "appid": API_KEY, "units": units_param}
    response = requests.get(FORECAST_URL, params=params)
    return response.json(), response.status_code

def format_time(ts):
    return datetime.fromtimestamp(ts).strftime("%I:%M %p")

def get_background(weather_desc, is_day=True):
    """Return CSS for background based on weather type."""
    weather_desc = weather_desc.lower()
    if "rain" in weather_desc:
        return "https://i.gifer.com/7VE.gif"  # animated rain
    if "cloud" in weather_desc:
        return "https://i.gifer.com/7Ryw.gif"  # animated clouds
    if "snow" in weather_desc:
        return "https://i.gifer.com/7QZn.gif"  # animated snow
    if "thunder" in weather_desc:
        return "https://i.gifer.com/7VE.gif"  # lightning
    if "clear" in weather_desc:
        return "https://i.gifer.com/7V9.gif" if is_day else "https://i.gifer.com/7V7.gif"
    if "mist" in weather_desc or "fog" in weather_desc:
        return "https://i.gifer.com/7RzC.gif"  # fog
    return "https://i.gifer.com/7V9.gif"  # default sunny

# ==============================
# Main App Logic
# ==============================
tab1, tab2 = st.tabs(["🌦 Current Weather", "📈 5-Day Forecast"])

if city_input:
    weather_data, w_status = fetch_weather(city_input)
    forecast_data, f_status = fetch_forecast(city_input)

    if w_status == 200 and f_status == 200:
        city_name = weather_data['name']
        country = weather_data['sys']['country']
        sunrise = weather_data['sys']['sunrise']
        sunset = weather_data['sys']['sunset']
        now = datetime.now().timestamp()
        is_day = sunrise <= now <= sunset

        condition = weather_data['weather'][0]['description'].title()
        icon = get_icon(condition, is_day)

        # ===== Set Animated Background =====
        bg_url = get_background(condition, is_day)
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url({bg_url});
                background-size: cover;
                background-attachment: fixed;
            }}
            </style>
            """, unsafe_allow_html=True
        )

        # ===== Current Weather Tab =====
        with tab1:
            st.subheader(f"🌆 Weather in {city_name}, {country}")
            st.markdown(f"### {icon} {condition}")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("🌡 Temperature", f"{weather_data['main']['temp']}°")
                st.metric("🤒 Feels Like", f"{weather_data['main']['feels_like']}°")
                st.metric("💧 Humidity", f"{weather_data['main']['humidity']}%")
            with col2:
                st.metric("🌬 Wind Speed", f"{weather_data['wind']['speed']} {'m/s' if units_param=='metric' else 'mph'}")
                st.metric("🌡 Pressure", f"{weather_data['main']['pressure']} hPa")
                st.metric("☀️ Sunrise", format_time(sunrise))
                st.metric("🌙 Sunset", format_time(sunset))

        # ===== Forecast Tab =====
        with tab2:
            st.subheader(f"📈 5-Day Forecast for {city_name}, {country}")
            df = pd.DataFrame({
                "Date": [f['dt_txt'] for f in forecast_data['list']],
                "Temperature": [f['main']['temp'] for f in forecast_data['list']],
                "Feels Like": [f['main']['feels_like'] for f in forecast_data['list']]
            })
            fig = px.line(df, x="Date", y=["Temperature", "Feels Like"], markers=True, title="🌡 Temperature vs Time")
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("📋 Show Forecast Data Table"):
                st.dataframe(df)

    else:
        st.error("❌ City not found or API error!")
else:
    st.info("⚠️ Enter a city to see the weather forecast.")
