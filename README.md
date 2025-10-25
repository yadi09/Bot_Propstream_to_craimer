# Propstream Automation Bot

Automates tasks between **Propstream** and **Craimer** using Playwright, Schedule, and Poetry.

## Tech Stack
- Python 3.11+
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

2. **Clone Repo**  
```bash
git clone https://github.com/<your-username>/propstream-bot.git
cd propstream-bot

3. **Install Python dependencies**  
```bash
poetry install

4. **Install Playwright browsers**  
```bash
poetry run playwright install chromium

5. **Create .env file in project root with your credentials:**  
```bash
LOGIN_URL=https://login.propstream.com/
TEST_USERNAME="your propstream email"
TEST_PASSWORD="your propstream password"
CRM_WEBHOOK_URL=http://localhost:8000/webhook
HEADLESS=1
FETCH_INTERVAL_MINUTES=1

6. **Run the bot**  
```bash
poetry run python -m bot.main
