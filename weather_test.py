import requests

API_KEY = "a97fd12f6837909eb8dcb30ef64f7c64"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

city = input("Enter city name: ")

params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric"
}

response = requests.get(BASE_URL, params=params)
data = response.json()

if response.status_code == 200:
    print(f"\n✅ Weather data for {data['name']}, {data['sys']['country']}")
    print(f"🌡️ Temperature: {data['main']['temp']}°C")
    print(f"💧 Humidity: {data['main']['humidity']}%")
    print(f"🌬️ Wind Speed: {data['wind']['speed']} m/s")
    print(f"🌤️ Condition: {data['weather'][0]['description'].title()}")
else:
    print(f"\n❌ Error: {data.get('message', 'City not found!')}")
