# ----- Geocoding using Nominatim -----
def get_coordinates(city_name: str) -> Optional[Tuple[float, float]]:
    """
    Get latitude and longitude for a city using the Nominatim API.
    Returns (lat, lon) or None if city not found or on error.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "WeatherScript/1.0 (contact@example.com)"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data:
            return None
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon
    except requests.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None

# ----- Weather using OpenWeather -----
def get_weather(lat: float, lon: float, api_key: str, units: str = "metric") -> Optional[Dict[str, Any]]:
    """
    Query the OpenWeather current weather API for given coordinates.
    units: 'metric' (Celsius) or 'imperial' (Fahrenheit).
    Returns JSON dict on success, or None on error.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": units
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            # Print response text for debugging if needed
            print(f"Debug: Response status: {response.status_code}, Response text: {response.text}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

# ----- CLI usage (prints Celsius) -----
def main_cli():
    if len(sys.argv) != 2:
        print("Usage: python3 weather.py \"City Name\"")
        sys.exit(1)

    city_name = sys.argv[1]
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("Error: OPENWEATHER_API_KEY environment variable not set")
        sys.exit(1)

    coords = get_coordinates(city_name)
    if not coords:
        print(f"Error: City '{city_name}' not found")
        sys.exit(1)

    lat, lon = coords
    weather_data = get_weather(lat, lon, api_key, units="metric")
    if not weather_data:
        print("Error: Failed to fetch weather data")
        sys.exit(1)

    temp_c = weather_data.get("main", {}).get("temp")
    conditions = weather_data.get("weather", [{}])[0].get("description", "unknown")

    print(f"City: {city_name}")
    print(f"Coordinates: {lat:.4f}, {lon:.4f}")
    if temp_c is not None:
        print(f"Temperature: {temp_c:.2f}°C")
    print(f"Conditions: {conditions}")

# ----- FastAPI application (returns Fahrenheit) -----
app = FastAPI(title="Weather API", description="Get weather information for cities")

@app.get("/weather/{city}")
async def get_weather_for_city(city: str):
    """
    Return JSON:
    {
      "city": <city>,
      "coordinates": { "latitude": <lat>, "longitude": <lon> },
      "temperature": "<value>°F",
      "conditions": "<description>"
    }
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenWeather API key not configured")

    coords = get_coordinates(city)
    if not coords:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")

    lat, lon = coords
    weather_data = get_weather(lat, lon, api_key, units="imperial")
    if not weather_data:
        raise HTTPException(status_code=500, detail="Failed to fetch weather data")

    temp_f = weather_data.get("main", {}).get("temp")
    conditions = weather_data.get("weather", [{}])[0].get("description", "unknown")

    return {
        "city": city,
        "coordinates": {
            "latitude": round(lat, 4),
            "longitude": round(lon, 4)
        },
        "temperature": f"{temp_f:.2f}°F" if temp_f is not None else None,
        "conditions": conditions
    }

# Allow running the CLI when invoked directly
if __name__ == "__main__":
    main_cli()
```

Important usage notes

<Callout icon="lightbulb">
  Note: Nominatim requires a valid User-Agent identifying your application. Respect their [usage policy](https://operations.osmfoundation.org/policies/nominatim/) and rate limits when making requests.
</Callout>

<Callout icon="warning">
  Warning: Never commit API keys to source control. Use environment variables (e.g., OPENWEATHER\_API\_KEY) and restrict keys where possible. Also monitor and respect API rate limits to avoid service interruptions.
</Callout>

Quick setup and run commands

| Step                        | Command                                             | Purpose                                                        |
| --------------------------- | --------------------------------------------------- | -------------------------------------------------------------- |
| Create venv                 | python3 -m venv venv                                | Create a virtual environment                                   |
| Activate venv (macOS/Linux) | source venv/bin/activate                            | Activate the venv                                              |
| Install deps                | pip install requests fastapi uvicorn                | Install required Python packages                               |
| Set API key                 | export OPENWEATHER\_API\_KEY="your\_api\_key\_here" | Provide OpenWeather credential                                 |
| Run CLI                     | python3 weather.py "New York"                       | Use script as a CLI (prints Celsius)                           |
| Run FastAPI server          | uvicorn weather:app --reload                        | Start server on [http://127.0.0.1:8000](http://127.0.0.1:8000) |

Example FastAPI request
GET [http://127.0.0.1:8000/weather/Forest%20Grove](http://127.0.0.1:8000/weather/Forest%20Grove)

Sample JSON response

```json theme={null}
{
  "city": "Forest Grove",
  "coordinates": {
    "latitude": 45.519,
    "longitude": -123.1111
  },
  "temperature": "60.76°F",
  "conditions": "overcast clouds"
}
```

Troubleshooting

* 401 Unauthorized from OpenWeather: ensure OPENWEATHER\_API\_KEY is set in the same environment where you run Python or uvicorn. New keys may take a few minutes to activate.
* City not found: Nominatim returned no results; verify spelling or try a larger query (e.g., include country).
* requests missing: ensure your virtual environment is active and run pip install requests.
* Python not found: use python3 on macOS/Linux if python points to Python 2.

Resources and References

| Resource                  | Description                                             | Link                                                                   |
| ------------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------- |
| Nominatim (OpenStreetMap) | Free geocoding to get coordinates from a city name      | [https://nominatim.org/](https://nominatim.org/)                       |
| OpenWeather API           | Current weather API used for temperature and conditions | [https://openweathermap.org/api](https://openweathermap.org/api)       |
| FastAPI                   | Python web framework used to expose the endpoint        | [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)         |
| requests                  | HTTP library used for external API requests             | [https://docs.python-requests.org/](https://docs.python-requests.org/) |

Suggested next steps

* Add caching for geocoding results to reduce Nominatim queries.
* Add input validation and rate limiting to the FastAPI app for production readiness.
* Containerize the app with Docker for easy deployment.
* Add tests for get\_coordinates and get\_weather functions to verify behavior with mocked HTTP responses.

This sequence demonstrates how Claude Code can scaffold working code, how to identify and debug small integration issues (API keys, headers, request params), and how to convert a simple script into a shareable HTTP API with FastAPI.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/3e896e50-3c07-4fdc-8603-bf125255d0a9/lesson/5681f91d-7538-4d69-80d9-f9848600103d" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/3e896e50-3c07-4fdc-8603-bf125255d0a9/lesson/2966483e-d854-40d5-acbd-023cce64e482" />
</CardGroup>


# Demo Writing Effective Development Prompts

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Working-with-Claude-Code/Demo-Writing-Effective-Development-Prompts/page

How to write clear, complete development prompts that produce predictable, secure, and maintainable code with examples and a sample Express.js JWT login implementation

In this lesson you’ll learn how to write development prompts that produce predictable, secure, and maintainable code from an AI assistant. Clear, specific prompts reduce incorrect assumptions, unnecessary back-and-forth, and security oversights.

<Frame>
  <img alt="A presentation slide reading &#x22;Writing effective development prompts&#x22; on a light background with a dark curved panel on the right. The word &#x22;Demo&#x22; appears prominently on the dark panel." />
</Frame>

## Why vague prompts fail

When a prompt is vague, the assistant fills gaps with assumptions. Sometimes those guesses match your intent; often they do not. The minimal example below shows how ambiguity quickly leads to unintended behavior.

```text theme={null}
* Welcome to the assistant!

cwd: /Users/jeremy/Repos/Claude Code Course/Express-login-demo

> Make a login screen
```

Because the project folder contains "Express-login-demo", the assistant assumes an Express-based solution. It may begin exploring the repository and proposing an Express implementation — fine if that’s your intent, but problematic if you expected a different stack or a different authentication flow.

The assistant might try discovery commands like:

```bash theme={null}
find /Users/jeremy/Repos/Claude\ Code\ Course/Express-login-demo -type f -name "*.js" -o -name "*.json" -o -name "*.html" -o -name "*.css" | head -20
```

If the repository is empty, this leads to unnecessary exploration and follow-up questions, slowing development. Vague prompts also cause missing concerns (validation, error handling, security requirements) because the model must guess which constraints matter to you.

## A better prompt — be explicit about intent and constraints

A good prompt explicitly states the stack, the endpoint, validation rules, authentication expectations, and desired responses. This reduces ambiguity and lets the assistant produce runnable code with fewer clarifications.

Example improved prompt:

```text theme={null}
Create a POST /api/auth/login endpoint using Express.js with the following requirements:

Input:
- email (string, required, must be a valid email)
- password (string, required, min 8 characters)

Process:
- Validate input using express-validator
- Check if user exists in PostgreSQL database
- Compare password using bcrypt
- Generate JWT token with 24h expiration

Response:
- Success: { token, user: { id, email, name } }
- Failure: Appropriate error message and status code

Include error handling for database failures and validation errors.
```

Because this prompt specifies technology, validation, security, and responses, the assistant can generate a complete implementation with far fewer clarifying questions.

## Example project changes the assistant might create

Below are concise, corrected snippets that implement the requirements above. These files illustrate a minimal but production-minded Express + PostgreSQL + JWT authentication flow.

package.json (created by initialization)

```json theme={null}
{
  "name": "express-login-demo",
  "version": "1.0.0",
  "description": "Express.js login demo with JWT authentication",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": ["express", "login", "jwt", "authentication"],
  "dependencies": {
    "bcrypt": "^5.0.1",
    "express": "^4.18.2",
    "express-validator": "^6.14.3",
    "jsonwebtoken": "^9.0.0",
    "pg": "^8.11.0",
    "dotenv": "^16.0.0"
  }
}
```

.env (example)

```text theme={null}
PORT=3000
JWT_SECRET=your_jwt_secret_key_here
JWT_EXPIRES_IN=24h
