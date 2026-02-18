from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from datetime import datetime
import traceback
from bot.logger import setup_logger
import httpx
from bot.jobs import run_tenant
from bot.tenants import load_tenants

app = FastAPI(title="PropStream Automation API", version="1.0.0")

logger = setup_logger()

# @app.post("/webhook")
# async def webhook(request: Request):
#     """Receive webhook data and append it to a JSON file asynchronously"""
#     try:
#         data = await request.json()
#         logger.info(f"Webhook received at {datetime.now().isoformat()} with {len(data)} keys")
#         logger.info(f"Full webhook data: {data}")

#         tenant_id = data.get("tenant_id") or data.get("tenantId")
#         if not tenant_id:
#             raise HTTPException(status_code=400, detail="tenant_id is required")

#         tenants = load_tenants()
#         tenant = next((t for t in tenants if t.get("id") == tenant_id), None)
#         if not tenant:
#             raise HTTPException(status_code=404, detail="Tenant not found")

#         inbound_webhook_url = tenant.get("crm", {}).get("inbound_webhook_url")
#         if not inbound_webhook_url:
#             raise HTTPException(status_code=500, detail="Missing tenant crm.inbound_webhook_url")

#         # Send the data to another api (inbound webhook)
#         async with httpx.AsyncClient() as client:
#             response = await client.post(inbound_webhook_url, json=data)
#             if response.status_code == 200:
#                 logger.info("✅ Successfully sent data to inbound webhook.")
#             else:
#                 logger.error(f"❌ Failed to send data to inbound webhook: {response.status_code} {response.text}")

#         return {"status": "success", "message": "Data received and being processed."}

#     except Exception as e:
#         logger.error(f"❌ Webhook error: {e}\n{traceback.format_exc()}")
#         raise HTTPException(status_code=400, detail=str(e))

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

def _run_tenant_job(tenant):
    try:
        run_tenant(tenant)
    except Exception as e:
        tenant_name = tenant.get("name", tenant.get("id", "unknown"))
        logger.exception(f"Error running tenant job: {tenant_name}. {e}")

@app.post("/pullData")
async def pull_data(request: Request, background_tasks: BackgroundTasks):
    """Run a single tenant job by tenant_id (scheduler_id must match if provided)."""
    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON body: {e}")

    tenant_id = data.get("tenant_id") or data.get("tenantId")
    scheduler_id = data.get("scheduler_id") or data.get("schedulerId")

    if not tenant_id:
        raise HTTPException(status_code=400, detail="tenant_id is required")

    if scheduler_id and scheduler_id != tenant_id:
        raise HTTPException(status_code=400, detail="scheduler_id must match tenant_id")

    tenants = load_tenants()
    tenant = next((t for t in tenants if t.get("id") == tenant_id), None)

    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    background_tasks.add_task(_run_tenant_job, tenant)
    return {
        "status": "accepted",
        "message": "Tenant job queued",
        "tenant_id": tenant_id,
    }
