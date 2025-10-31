# Propstream Automation Bot

Automates tasks between **Propstream** and **Craimer** using Playwright, Schedule, and Poetry.

## Tech Stack
- Python 3.12+
- Poetry (dependency & environment management)
- Playwright (Chromium browser)
- Schedule (job scheduling)
- python-dotenv (environment variables)
- Requests (HTTP requests)

## Setup

1. **Install Poetry**  
```bash
curl -sSL https://install.python-poetry.org | python3 -
poetry --version
```
2. **Clone Repo**  
```bash
git clone https://github.com/yadi09/propstream-bot.git
cd propstream-bot
```
3. **Install Python dependencies**  
```bash
poetry install
```
4. **Install Playwright browsers**  
```bash
poetry run playwright install chromium
```
5. **Create .env file in project root with your credentials:**  
```bash
LOGIN_URL=https://login.propstream.com/
TEST_USERNAME="your propstream email"
TEST_PASSWORD="your propstream password"
CRM_WEBHOOK_URL="Craimer_api" # To upload the csv file to specific Sub-acc
HEADLESS=1
```
6. **Run the bot**  
```bash
poetry run python -m bot.main
```

## Setup (Docker)

**Build the Docker image**

```bash
docker build -t project-name .
docker run --env-file .env project-name
```

## A complate process of the bot (logs):
```bash
yadi0988@DESKTOP-6RQVMIA:/mnt/d/Shad Project (GHL)/GHL Tasks/Task 6 (propstream Automation)/Bot - Propstream to Craimer/propstream_bot$ poetry run python3 -m bot.main
2025-10-30 20:53:30 [INFO] 🚀 Starting PropStream Automation (API + Scheduler)...
2025-10-30 20:53:30 [INFO] Starting FastAPI API server...
2025-10-30 20:53:30 [INFO] ✅ Both API and Scheduler started successfully.
2025-10-30 20:53:30 [INFO] Starting scheduler service...
2025-10-30 20:53:30 [INFO] Scheduler started [runs every Sunday at 10:00].
2025-10-30 20:53:30 [INFO] --> Starting scheduled fetch job...
2025-10-30 20:53:30 [INFO] Launching browser to retrieve PropStream token...
INFO:     Started server process [18437]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
2025-10-30 20:53:31 [INFO] Navigating to login page...
2025-10-30 20:53:35 [INFO] Waiting for login to complete...
2025-10-30 20:54:09 [INFO] [✅] Token captured from https://app.propstream.com/eqbackend/resource/auth/ps4/map/statistics/metrics
2025-10-30 20:54:14 [INFO] Token saved to token.txt
2025-10-30 20:54:19 [INFO] Successfully fetched All marketing lists.
2025-10-30 20:54:19 [WARNING] Today's marketing list not found.
2025-10-30 20:54:19 [ERROR] ❌ Could not retrieve marketing list ID.
2025-10-30 20:54:19 [INFO] Creating a today's marketing list...
2025-10-30 20:54:23 [INFO] Add to marketing list response 1 status: 200
2025-10-30 20:54:29 [INFO] Add to marketing list response 2 status: 200
2025-10-30 20:54:33 [INFO] Add to marketing list response 3 status: 200
2025-10-30 20:54:38 [INFO] Add to marketing list response 4 status: 200
2025-10-30 20:54:42 [INFO] Add to marketing list response 5 status: 200
2025-10-30 20:54:47 [INFO] Add to marketing list response 6 status: 200
2025-10-30 20:54:52 [INFO] Add to marketing list response 7 status: 200
2025-10-30 20:54:58 [INFO] Add to marketing list response 8 status: 200
2025-10-30 20:55:02 [INFO] Add to marketing list response 9 status: 200
2025-10-30 20:55:08 [INFO] Add to marketing list response 10 status: 200
2025-10-30 20:55:15 [INFO] Add to marketing list response 11 status: 200
2025-10-30 20:55:19 [INFO] Add to marketing list response 12 status: 200
2025-10-30 20:55:24 [INFO] Add to marketing list response 13 status: 200
2025-10-30 20:55:29 [INFO] Successfully fetched All marketing lists.
2025-10-30 20:55:29 [INFO] Found today's marketing list ID: 4996559
2025-10-30 20:55:29 [INFO] Fetching property data from PropStream API...
2025-10-30 20:55:34 [INFO] Fetched 280 properties.
2025-10-30 20:55:42 [INFO] ✅ Data successfully sent to CRM (202)
2025-10-30 20:55:42 [INFO] Response: {"message":"Lead uploading to crm has started. Processing 279 leads. Estimated time: 1m 23s. You can check the logs for progress."}
2025-10-30 20:55:42 [INFO] Waiting for the next scheduled job...
```