from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import logging

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    WEATHER_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()

# Get API key from environment variables
# WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_KEY = settings.WEATHER_API_KEY
if not WEATHER_API_KEY:
    logging.error("No WEATHER_API_KEY found in environment variables")
    raise ValueError("WEATHER_API_KEY environment variable is required")

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    condition: str
    humidity: int = None
    wind_speed: float = None

@app.get("/api/weather", response_model=WeatherResponse)
async def get_weather(city: str = Query(..., description="City name to get weather for")):
    """
    Get current weather for a specified city.
    Uses OpenWeatherMap API to fetch weather data.
    """
    if not city:
        raise HTTPException(status_code=400, detail="City parameter is required")

    # Using WeatherAPI.com
    api_url = "https://api.weatherapi.com/v1/current.json"

    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "aqi": "no"  # Set to "yes" if you want air quality data
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, params=params)

            if response.status_code != 200:
                error_data = response.json()
                error_message = error_data.get("message", "Unknown error")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Weather API error: {error_message}"
                )

            weather_data = response.json()

            # Extract relevant data from WeatherAPI.com response format
            weather_response = WeatherResponse(
                city=weather_data["location"]["name"],
                temperature=weather_data["current"]["temp_c"],
                condition=weather_data["current"]["condition"]["text"],
                humidity=weather_data["current"]["humidity"],
                wind_speed=weather_data["current"]["wind_kph"]
            )

            return weather_response

    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Error communicating with Weather API: {str(e)}")

@app.get("/working")
async def health_check():
    return {"status": "yes working"}

if __name__ == "__main__":
    # For development purposes
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
