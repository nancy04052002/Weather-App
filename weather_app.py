import streamlit as st
import requests
from datetime import datetime

API_KEY = "a97fd12f6837909eb8dcb30ef64f7c64"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=a97fd12f6837909eb8dcb30ef64f7c64"

st.title("🌍 Real-Time Weather App")
st.markdown("🌦️ Enter a city name (with optional country code): e.g., `Paris,FR`, `Delhi,IN`, `Tokyo,JP`")

city = st.text_input("Enter City Name:")

if st.button("Get Weather"):
    if city:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            city_name = data['name']
            country = data['sys']['country']
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            wind_speed = data['wind']['speed']
            sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime("%I:%M %p")
            sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime("%I:%M %p")
            condition = data['weather'][0]['description'].title()
            icon = data['weather'][0]['icon']

            st.subheader(f"🌆 Weather in {city_name}, {country}")
            st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("🌡️ Temperature (°C)", f"{temp}°C")
                st.metric("🤒 Feels Like", f"{feels_like}°C")
                st.metric("💧 Humidity", f"{humidity}%")
            with col2:
                st.metric("🌬️ Wind Speed", f"{wind_speed} m/s")
                st.metric("🌡️ Pressure", f"{pressure} hPa")
                st.metric("☀️ Sunrise", sunrise)
                st.metric("🌙 Sunset", sunset)

            st.success(f"Weather Condition: **{condition}**")

        else:
            st.error(f"❌ Error: {data.get('message', 'City not found!')}")
    else:
        st.warning("Please enter a city name.")