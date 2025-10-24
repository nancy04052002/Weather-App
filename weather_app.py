import streamlit as st
import requests
from datetime import datetime

API_KEY = "a97fd12f6837909eb8dcb30ef64f7c64"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

st.title("🌍 Real-Time Weather App")
st.markdown("🌦️ Enter a city name (with optional country code): e.g., `Paris,FR`, `Delhi,IN`")

city = st.text_input("Enter City Name:")

if st.button("Get Weather"):
    if city:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            st.subheader(f"🌆 Weather in {data['name']}, {data['sys']['country']}")
            st.image(f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png")
            st.metric("🌡️ Temperature (°C)", f"{data['main']['temp']}°C")
            st.metric("🤒 Feels Like", f"{data['main']['feels_like']}°C")
            st.metric("💧 Humidity", f"{data['main']['humidity']}%")
            st.metric("🌬️ Wind Speed", f"{data['wind']['speed']} m/s")
            st.metric("🌡️ Pressure", f"{data['main']['pressure']} hPa")
            st.metric("☀️ Sunrise", datetime.fromtimestamp(data['sys']['sunrise']).strftime("%I:%M %p"))
            st.metric("🌙 Sunset", datetime.fromtimestamp(data['sys']['sunset']).strftime("%I:%M %p"))
            st.success(f"Weather Condition: **{data['weather'][0]['description'].title()}**")
        else:
            st.error(f"❌ Error: {data.get('message', 'City not found!')}")
    else:
        st.warning("Please enter a city name.")
