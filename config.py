import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNELS = [
    "UstozShogird",
    "UstozShogirdSohalar"
]

POST_TYPES = {
    "job": {
        "keyword": "ish joyi kerak:",
        "label": "Ish joyi kerak",
        "emoji": "👨‍💼"
    },
    "worker": {
        "keyword": "xodim kerak:",
        "label": "Xodim kerak",
        "emoji": "🏢"
    },
    "partner": {
        "keyword": "sherik kerak:",
        "label": "Sherik kerak",
        "emoji": "🏅"
    },
    "mentor": {
        "keyword": "ustoz kerak:",
        "label": "Ustoz kerak",
        "emoji": "🎓"
    },
    "student": {
        "keyword": "shogird kerak:",
        "label": "Shogird kerak",
        "emoji": "📚"
    }
}
