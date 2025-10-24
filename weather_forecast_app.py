import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

API_KEY = "a97fd12f6837909eb8dcb30ef64f7c64"  
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=a97fd12f6837909eb8dcb30ef64f7c64"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={a97fd12f6837909eb8dcb30ef64f7c64}&units=metric"

st.set_page_config(page_title="Weather App", page_icon="🌦", layout="centered")

st.title("🌍 Real-Time Weather & 5-Day Forecast App")
st.markdown("💡 **Example Inputs:** `Paris,FR` | `London,GB` | `Delhi,IN` | `New York,US`")

city = st.text_input("🏙️ Enter City Name (include country code, e.g. London,GB):")

def get_icon(weather):
    """Return an emoji for a given weather description."""
    weather = weather.lower()
    if "cloud" in weather:
        return "☁️"
    elif "rain" in weather:
        return "🌧"
    elif "clear" in weather:
        return "☀️"
    elif "snow" in weather:
        return "❄️"
    elif "thunder" in weather:
        return "⛈"
    elif "mist" in weather or "fog" in weather:
        return "🌫"
    else:
        return "🌈"


def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    return response.json(), response.status_code


def get_forecast(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(FORECAST_URL, params=params)
    return response.json(), response.status_code


if st.button("Get Weather Forecast"):
    if city:
        weather_data, status = get_weather(city)
        forecast_data, f_status = get_forecast(city)

        if status == 200 and f_status == 200:
            st.success(f"✅ Weather for **{weather_data['name']}**, {weather_data['sys']['country']}")
            condition = weather_data["weather"][0]["description"]
            icon = get_icon(condition)

            st.markdown(f"### {icon} {condition.title()}")
            st.write(f"🌡 **Temperature:** {weather_data['main']['temp']}°C")
            st.write(f"💧 **Humidity:** {weather_data['main']['humidity']}%")
            st.write(f"🌬 **Wind Speed:** {weather_data['wind']['speed']} m/s")
            st.write(f"📏 **Pressure:** {weather_data['main']['pressure']} hPa")
            st.write(f"🌅 **Sunrise:** {datetime.utcfromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S')} UTC")
            st.write(f"🌇 **Sunset:** {datetime.utcfromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S')} UTC")

            st.subheader("📈 5-Day Temperature Trend")

            forecast_list = forecast_data["list"]
            df = pd.DataFrame({
                "Date": [f["dt_txt"] for f in forecast_list],
                "Temperature (°C)": [f["main"]["temp"] for f in forecast_list],
                "Feels Like (°C)": [f["main"]["feels_like"] for f in forecast_list]
            })

            
            fig = px.line(
                df,
                x="Date",
                y=["Temperature (°C)", "Feels Like (°C)"], 
                title="🌡 Temperature vs Time",
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

            
            with st.expander("📋 Show Forecast Data Table"):
                st.dataframe(df)

        else:
            st.error("❌ City not found or API error! Please check your API key or city spelling.")
    else:
        st.warning("⚠️ Please enter a city name to continue.")