import os
from dotenv import load_dotenv

load_dotenv()

# URLs
LOGIN_URL = os.getenv("LOGIN_URL", "https://login.propstream.com/")

# Credentials
USERNAME = os.getenv("TEST_USERNAME")
PASSWORD = os.getenv("TEST_PASSWORD")

# CRM Webhook
CRM_WEBHOOK_URL = os.getenv("CRM_WEBHOOK_URL", "https://sms-api.craimer.com/api/v2/ghl/create_contact")

# Behavior
HEADLESS = os.getenv("HEADLESS", "1") != "0"  # 0 = show browser, 1 = headless

TOKEN_FILE = "token.txt"

# Multi-tenant config
TENANTS_CONFIG = os.getenv("TENANTS_CONFIG", "tenants.yml")
