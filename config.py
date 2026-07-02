from pathlib import Path
from dotenv import load_dotenv
import os
import logging

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Base Directory
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent

# -----------------------------
# App Configuration
# -----------------------------
APP_NAME = os.getenv("APP_NAME", "AI Recruitment Platform")
DEBUG = os.getenv("DEBUG", "False") == "True"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# -----------------------------
# Folder Paths
# -----------------------------
UPLOADS_DIR = BASE_DIR / "uploads"
REPORTS_DIR = BASE_DIR / "reports"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"
DATABASE_DIR = BASE_DIR / "database"
STATIC_DIR = BASE_DIR / "static"
ASSETS_DIR = BASE_DIR / "assets"

folders = [
    UPLOADS_DIR,
    REPORTS_DIR,
    DATA_DIR,
    MODELS_DIR,
    LOGS_DIR,
    DATABASE_DIR,
    STATIC_DIR,
    ASSETS_DIR,
]

for folder in folders:
    folder.mkdir(exist_ok=True)

# -----------------------------
# Database
# -----------------------------
DATABASE_PATH = DATABASE_DIR / "recruitment.db"

# -----------------------------
# Logging
# -----------------------------
LOG_FILE = LOGS_DIR / "app.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(APP_NAME)