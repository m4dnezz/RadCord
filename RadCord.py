import requests
import os
from arrapi import RadarrAPI

API_KEY = os.getenv("RADARR_API")
RADARR_URL = os.getenv("RADARR_URL")

if not API_KEY:
    raise ValueError("API key not found. Please make sure to set RADARR_API envoirment varialbe")

radarr = RadarrAPI(RADARR_URL, API_KEY)

