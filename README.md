# Propstream Automation Bot

Automates tasks between **Propstream** and **Craimer** using Playwright, FastAPI, and Poetry.

## Tech Stack

- Python 3.12+
- Poetry (dependency & environment management)
- Playwright (Chromium browser)
- FastAPI (webhook + job trigger API)
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

6. **Run the API server**

```bash
poetry run python -m bot.main
```

7. **Trigger a tenant job**

```bash
curl -s -X POST http://127.0.0.1:8000/pullData \
  -H "Content-Type: application/json" \
  -d '{"tenant_id":"<TENANT_ID>","scheduler_id":"<TENANT_ID>"}'
```

## Setup (Docker)

**Build the Docker image**

```bash
docker build -t project-name .
docker run --env-file .env project-name
```

## AWS Free Trial Hosting (API + Cron)

This guide uses an EC2 free-tier instance plus cron to call the API on Monday/Thursday and a systemd service for the webhook API.

If you prefer Docker (you already have a Dockerfile), use the Docker option below.

### 1) Launch a free-tier EC2 instance

- AMI: Ubuntu 22.04 LTS
- Instance type: t3.micro or t2.micro (free tier)
- Storage: 20 GB gp3 (free tier)
- Security Group:
  - Inbound: allow TCP 22 from your IP (SSH)
  - Inbound: allow TCP 8000 from your IP only (if you want to test the webhook)
  - Optional: if the webhook must be reachable from the internet, open TCP 8000 to 0.0.0.0/0 and lock it down with a reverse proxy and HTTPS

SSH into the instance:

```bash
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### 2) Install system dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3.12 python3.12-venv python3-pip git
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Install Playwright browsers and deps later, after the repo is cloned.

### 2B) Docker option (recommended if you want to use the Dockerfile)

Install Docker and Docker Compose:

```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-plugin
sudo usermod -aG docker ubuntu
newgrp docker
```

### 3) Clone and install the project

```bash
sudo mkdir -p /opt/propstream_bot
sudo chown -R ubuntu:ubuntu /opt/propstream_bot
git clone <YOUR_REPO_URL> /opt/propstream_bot
cd /opt/propstream_bot
poetry install
poetry run playwright install chromium --with-deps
```

### 3B) Docker build (Docker option)

```bash
sudo mkdir -p /opt/propstream_bot
sudo chown -R ubuntu:ubuntu /opt/propstream_bot
git clone <YOUR_REPO_URL> /opt/propstream_bot
cd /opt/propstream_bot
docker build -t propstream-bot:latest .
```

### 4) Create environment file

Create a system-wide env file that cron and systemd can load:

```bash
sudo tee /etc/propstream_bot.env > /dev/null << 'EOF'
LOGIN_URL=https://login.propstream.com/
PALM_PS_USER=your_propstream_user
PALM_PS_PASS=your_propstream_pass
CLEAR_PS_USER=your_propstream_user
CLEAR_PS_PASS=your_propstream_pass
REG_PS_USER=your_propstream_user
REG_PS_PASS=your_propstream_pass
CRM_WEBHOOK_URL=https://sms-api.craimer.com/api/v2/ghl/create_contact
HEADLESS=1
TENANTS_CONFIG=/opt/propstream_bot/tenants.yml
EOF
```

If you use Docker, this same file can be passed to `docker run --env-file` or loaded by systemd.

### 5) Trigger tenant jobs with cron (Mon & Thu)

Edit root crontab:

```bash
sudo crontab -e
```

Add this entry (runs at 10:00 AM New York time):

```bash
SHELL=/bin/bash
CRON_TZ=America/New_York
0 10 * * 1,4 . /etc/propstream_bot.env; curl -s -X POST http://127.0.0.1:8000/pullData -H "Content-Type: application/json" -d '{"tenant_id":"<TENANT_ID>","scheduler_id":"<TENANT_ID>"}' >> /var/log/propstream_bot.log 2>&1
```

If you want a different time, adjust the `0 10` part and the `CRON_TZ` value.

If you use Docker, replace the cron command with:

```bash
SHELL=/bin/bash
CRON_TZ=America/New_York
0 10 * * 1,4 . /etc/propstream_bot.env; curl -s -X POST http://127.0.0.1:8000/pullData -H "Content-Type: application/json" -d '{"tenant_id":"<TENANT_ID>","scheduler_id":"<TENANT_ID>"}' >> /var/log/propstream_bot.log 2>&1
```

### 6) Run the webhook API as a service (systemd)

Create a systemd unit:

```bash
sudo tee /etc/systemd/system/propstream_webhook.service > /dev/null << 'EOF'
[Unit]
Description=Propstream Webhook API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/propstream_bot
EnvironmentFile=/etc/propstream_bot.env
ExecStart=/home/ubuntu/.local/bin/poetry run uvicorn bot.api:app --host 0.0.0.0 --port 8000
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

Enable and start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable propstream_webhook.service
sudo systemctl start propstream_webhook.service
sudo systemctl status propstream_webhook.service
```

### 6B) Run the webhook API in Docker (Docker option)

Create a systemd unit that runs the container:

```bash
sudo tee /etc/systemd/system/propstream_webhook.service > /dev/null << 'EOF'
[Unit]
Description=Propstream Webhook API (Docker)
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/propstream_bot
EnvironmentFile=/etc/propstream_bot.env
ExecStart=/usr/bin/docker run --rm --name propstream-webhook -p 8000:8000 --env-file /etc/propstream_bot.env propstream-bot:latest uvicorn bot.api:app --host 0.0.0.0 --port 8000
ExecStop=/usr/bin/docker stop propstream-webhook
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

Then enable and start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable propstream_webhook.service
sudo systemctl start propstream_webhook.service
sudo systemctl status propstream_webhook.service
```

### 7) Verify

- Cron log: `/var/log/propstream_bot.log`
- Webhook logs: `sudo journalctl -u propstream_webhook.service -f`
