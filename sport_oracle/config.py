import os

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
FOOTBALL_DATA_API_KEY = os.environ["FOOTBALL_DATA_API_KEY"]

FOOTBALL_DATA_BASE_URL = "https://api.football-data.org/v4"

SUPPORTED_COMPETITIONS = {
    "PL": "Premier League",
    "PD": "La Liga",
    "BL1": "Bundesliga",
    "SA": "Serie A",
    "FL1": "Ligue 1",
    "CL": "Champions League",
    "EC": "European Championship",
    "WC": "World Cup",
}

GEMINI_MODEL = "gemini-1.5-flash-latest"
