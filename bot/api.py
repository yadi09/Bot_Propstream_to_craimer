from fastapi import FastAPI, HTTPException, Request
from datetime import datetime
import traceback
from bot.logger import setup_logger
import httpx

app = FastAPI(title="PropStream Automation API", version="1.0.0")
logger = setup_logger()

@app.post("/webhook")
async def webhook(request: Request):
    """Receive webhook data and append it to a JSON file asynchronously"""
    try:
        data = await request.json()
        logger.info(f"Webhook received at {datetime.now().isoformat()} with {len(data)} keys")
        logger.info(f"Full webhook data: {data}")

        # Send the data to another api (inbound webhook)
        async with httpx.AsyncClient() as client:
            response = await client.post("https://services.leadconnectorhq.com/hooks/S9g9sAgRoWUU9jp0M5Bi/webhook-trigger/bb05c8f7-6b1f-4764-833d-843e927f9f32", json=data)
            if response.status_code == 200:
                logger.info("✅ Successfully sent data to inbound webhook.")
            else:
                logger.error(f"❌ Failed to send data to inbound webhook: {response.status_code} {response.text}")

        return {"status": "success", "message": "Data received and being processed."}

    except Exception as e:
        logger.error(f"❌ Webhook error: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))
