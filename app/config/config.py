import json
from pathlib import Path
from functools import lru_cache

SETTINGS_FILE = Path("app/config/settings.json")

@lru_cache()
def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)
    raise FileNotFoundError("Settings file not found. Run the API to initialize one.")
