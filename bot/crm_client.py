import requests
from bot.config import CRM_WEBHOOK_URL
from bot.logger import setup_logger

logger = setup_logger("crm_client")

def send_to_crm(data):
    if not data:
        logger.warning("No data to send to CRM.")
        return
    try:
        response = requests.post(CRM_WEBHOOK_URL, json=data)
        if response.status_code in [200, 201, 202]:
            logger.info(f"✅ Data successfully sent to CRM ({response.status_code})")
        else:
            logger.error(f"CRM webhook error ({response.status_code}): {response.text}")
    except Exception as e:
        logger.exception(f"Error sending data to CRM: {e}")
