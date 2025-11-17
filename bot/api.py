from fastapi import FastAPI, HTTPException, Request
from datetime import datetime
import traceback
from bot.logger import setup_logger
from bot.get_comps import get_comps_for_address 
import httpx
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",     
    "http://127.0.0.1:5173",
]


app = FastAPI(title="PropStream Automation API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # List of origins to allow
    allow_credentials=True,            # Allow cookies to be sent
    allow_methods=["*"],               # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],               # Allow all headers
)

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

@app.get("/comps")
def get_comps(address: str = None):
    """Endpoint to get property comps for a given address"""
    if not address:
        logger.error("❌ Address query parameter is missing.")
        raise HTTPException(status_code=400, detail="Address query parameter is required")
    try:
        logger.info(f'Received request for comps of address: {address}')
        comps_data = get_comps_for_address(address)  # Assume this function is defined elsewhere
        return {"status": "success", "data": comps_data}
    except Exception as e:
        logger.error(f"❌ Error getting comps for address {address}: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Error retrieving comps data")
