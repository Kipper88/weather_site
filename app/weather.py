import httpx

async def get_forecast(city: str):
    async with httpx.AsyncClient() as client:
        geo_resp = await client.get("https://geocoding-api.open-meteo.com/v1/search", params={"name": city})
        geo_data = geo_resp.json()
        if not geo_data.get("results"):
            return {"error": "Город не найден"}

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        weather_resp = await client.get("https://api.open-meteo.com/v1/forecast", params={
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        })

        return weather_resp.json().get("current_weather", {"error": "Ошибка получения прогноза"})