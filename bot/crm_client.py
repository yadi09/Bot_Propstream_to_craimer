import json
import requests
from bot.config import CRM_WEBHOOK_URL
from bot.logger import setup_logger
from io import BytesIO, StringIO
import csv

logger = setup_logger("crm_client")

# def send_to_crm(data):
#     if not data:
#         logger.warning("No data to send to CRM.")
#         return
#     try:
#         response = requests.post(CRM_WEBHOOK_URL, json=data)
#         if response.status_code in [200, 201, 202]:
#             logger.info(f"✅ Data successfully sent to CRM ({response.status_code})")
#         else:
#             logger.error(f"CRM webhook error ({response.status_code}): {response.text}")
#     except Exception as e:
#         logger.exception(f"Error sending data to CRM: {e}")

CRM_API_URL = "https://sms-api.craimer.com/api/v2/ghl/create_contact"
USERNAME = "bot_user"
TAGS = ["propstream"]

def generate_csv_from_json(data):
    """
    Generate CSV from property data and internal mapping JSON.
    Returns a BytesIO object (ready to upload via requests).
    """
    properties = data.get("properties", [])
    mapping_data = data.get("mapping_data", {})
    mapping = mapping_data.get("valueCols", [])
    
    columns = [col["colId"] for col in mapping]
    headers = [col["headerName"] for col in mapping]

    # Use StringIO for CSV writing (text)
    text_output = StringIO()
    writer = csv.DictWriter(text_output, fieldnames=headers)
    writer.writeheader()

    for prop in properties:
        row = {}
        for col in mapping:
            col_id = col["colId"]
            header = col["headerName"]
            row[header] = prop.get(col_id, "")
        writer.writerow(row)

    # Convert text buffer to bytes for upload
    byte_output = BytesIO(text_output.getvalue().encode("utf-8"))
    byte_output.seek(0)
    return byte_output


def send_to_crm(data, tenant_id):
    """Send generated CSV + mapping data to CRM API."""
    if not data:
        logger.warning("No data to send to CRM.")
        return
    
    try:
        # 1 Generate the CSV file in-memory
        csv_file = generate_csv_from_json(data)

        # You can pass only the "map_data" portion for the API
        map_data = {
            "first_name": "MLS Agent Name",
            "last_name": "MLS Agent Name",
            "phone_number": "MLS Agent Phone",
            "email": "MLS Agent E-Mail"
        }

        # 3️ Prepare form data for multipart upload
        files = {
            "new_members_file": ("properties.csv", csv_file, "text/csv")
        }
        data_payload = {
            "map_data": json.dumps(map_data),
            "username": USERNAME,
            "tags": json.dumps(TAGS)
        }

        # 4️ Send POST request
        response = requests.post(
            f"{CRM_API_URL}?tenant_id={tenant_id}",
            files=files,
            data=data_payload
        )

        # 5️ Log result
        if response.status_code in [200, 201, 202]:
            logger.info(f"✅ Data successfully sent to CRM ({response.status_code})")
            logger.info(f"Response: {response.text}")
        else:
            logger.error(f"❌ CRM webhook error ({response.status_code}): {response.text}")

    except Exception as e:
        logger.exception(f"Error sending data to CRM: {e}")
