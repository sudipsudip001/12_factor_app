import { useState } from "react";
import "./App.css";

function App() {
  const [weather, setWeather] = useState(null);
  const [city, setCity] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!city.trim()) {
      setError("Please enter a city name");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Send request to your FastAPI backend
      const response = await fetch(
        `/api/weather?city=${encodeURIComponent(city)}`
      );

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      setWeather(data);
    } catch (err) {
      setError(`Failed to fetch weather data: ${err.message}`);
      setWeather(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="weather-app">
      <h1>Weather App</h1>

      <form onSubmit={handleSubmit}>
        <label>
          Enter the city name: <br />
          <input
            type="text"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            placeholder="e.g., London"
          />
        </label>
        <br />
        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "See weather"}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {weather && (
        <div className="weatherData">
          <h2>Weather in {weather.city}</h2>
          <div className="weather-info">
            <p>
              <strong>Temperature:</strong> {weather.temperature}°C
            </p>
            <p>
              <strong>Condition:</strong> {weather.condition}
            </p>
            {weather.humidity && (
              <p>
                <strong>Humidity:</strong> {weather.humidity}%
              </p>
            )}
            {weather.wind_speed && (
              <p>
                <strong>Wind:</strong> {weather.wind_speed} km/h
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
