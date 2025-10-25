import os
from dotenv import load_dotenv

load_dotenv()

# URLs
LOGIN_URL = os.getenv("LOGIN_URL", "https://login.propstream.com/")
BASE_API_URL = os.getenv("BASE_API_URL", "https://app.propstream.com/eqbackend/resource/auth/ps4/user/properties")

# Credentials
USERNAME = os.getenv("TEST_USERNAME")
PASSWORD = os.getenv("TEST_PASSWORD")

# CRM Webhook
CRM_WEBHOOK_URL = os.getenv("CRM_WEBHOOK_URL", "http://localhost:8000/webhook")

# Behavior
HEADLESS = os.getenv("HEADLESS", "1") != "0"  # 0 = show browser, 1 = headless
FETCH_INTERVAL_MINUTES = int(os.getenv("FETCH_INTERVAL_MINUTES", "1")) # in minutes

# Paths
DATA_DIR = "data/all_data"
LOG_DIR = "logs"
TOKEN_FILE = "token.txt"
