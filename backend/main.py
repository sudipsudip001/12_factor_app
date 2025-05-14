from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging

WEATHER_API_KEY = os.getenv("../WEATHER_API_KEY")
if not WEATHER_API_KEY:
    logging.error("No WEATHER_API_KEY found in environment variables")
    raise ValueError("WEATHER_API_KEY environment variable is required")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    condition: str
    humidity: int = None
    wind_speed: float = None

@app.get("/")
def hello():
    return {"hello world"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
