from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from datetime import datetime
import json
import os
import traceback
from bot.logger import setup_logger

app = FastAPI(title="PropStream Automation API", version="1.0.0")
logger = setup_logger("api")

# Ensure data directory exists
DATA_DIR = "received_data"
os.makedirs(DATA_DIR, exist_ok=True)
FILE_PATH = os.path.join(DATA_DIR, "webhook_data.json")

@app.get("/")
def root():
    logger.info("Root endpoint hit — API is running")
    return {"message": "✅ API is running", "version": "1.0.0"}

@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    """Receive webhook data and append it to a JSON file asynchronously"""
    try:
        data = await request.json()
        logger.info(f"Webhook received at {datetime.now().isoformat()} with {len(data)} keys")

        # Save asynchronously
        background_tasks.add_task(save_data_to_file, data)
        return {"status": "success", "message": "Data received and being processed."}

    except Exception as e:
        logger.error(f"❌ Webhook error: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))

def save_data_to_file(data: dict):
    """Append received data to a local JSON file safely"""
    try:
        logger.info("Saving received webhook data to file...")

        # Load existing data
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r") as f:
                existing = json.load(f)
        else:
            existing = []

        # Append new record with timestamp
        existing.append({
            "timestamp": datetime.now().isoformat(),
            "data": data
        })

        # Save back
        with open(FILE_PATH, "w") as f:
            json.dump(existing, f, indent=4)

        logger.info(f"✅ Webhook data appended to {FILE_PATH}")

    except Exception as e:
        logger.error(f"❌ Failed to save webhook data: {e}\n{traceback.format_exc()}")
