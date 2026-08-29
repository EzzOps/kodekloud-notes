# Demo Working with APIs and External Services

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Working-with-Claude-Code/Demo-Working-with-APIs-and-External-Services/page

Demonstrates building a Python script and FastAPI service that geocodes cities with Nominatim and fetches current weather from OpenWeather using an environment API key

In this lesson we demonstrate two practical ways Claude Code helps when working with external APIs:

* Generate a Python script that looks up a city's coordinates with Nominatim and fetches current weather from OpenWeather.
* Convert that script into a FastAPI application so others can request weather for a city via HTTP.

<Frame>
  <img alt="A presentation slide titled &#x22;Working with APIs and External Services&#x22; with a dark curved shape on the right containing the word &#x22;Demo&#x22; in blue. A small &#x22;© Copyright KodeKloud&#x22; note appears in the bottom-left." />
</Frame>

Overview of the final deliverable

* A single, runnable Python file (weather.py) that:
  * Accepts a city name
  * Uses Nominatim to resolve latitude/longitude
  * Uses OpenWeather to fetch current weather (API key read from OPENWEATHER\_API\_KEY)
  * Provides a CLI entrypoint (prints Celsius)
  * Exposes a FastAPI endpoint /weather/ that returns Fahrenheit JSON

Complete, consolidated, and runnable weather.py

```python theme={null}
#!/usr/bin/env python3
import os
import sys
from typing import Optional, Tuple, Dict, Any

import requests
from fastapi import FastAPI, HTTPException
