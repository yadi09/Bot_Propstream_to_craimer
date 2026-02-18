from datetime import datetime
import json
import requests
from bot.config import CRM_WEBHOOK_URL
from bot.logger import setup_logger
from io import BytesIO, StringIO
import csv

logger = setup_logger()

# USERNAME = "bot_user"
# current_datetime = datetime.now()
# date_tag = f"{current_datetime.strftime('%m/%d/%y')}"
# TAGS = ["Craimer_bot", date_tag, "padsplit"]
DEFAULT_USERNAME = "bot_user"

def generate_csv_from_json(data):
    """
    Generate CSV from property data.
    Returns a BytesIO object (ready to upload via requests).
    """
    properties = data.get("properties", [])
    mapping_data = data.get("mapping_data", {})
    mapping = mapping_data.get("valueCols", [])
    
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
    byte_output.seek(0) # Reset pointer to start
    return byte_output


# def send_to_crm(data, tenant_id):
def send_to_crm(data, tenant):
    """Send generated CSV + mapping data to CRM API."""
    if not data:
        logger.warning("No data to send to CRM.")
        return
    
    try:
        # 1 Generate the CSV file in-memory
        csv_file = generate_csv_from_json(data)

        # map_data = {
        #     "first_name": "MLS Agent Name",
        #     "last_name": "MLS Agent Name",
        #     "phone_number": "MLS Agent Phone",
        #     "email": "MLS Agent E-Mail",
        #     "Property Address": "Address",
        #     "Unit": "Unit #",
        #     "Property City": "City",
        #     "Property State": "State",
        #     "Property Zip": "Zip",
        #     "Property County": "County",
        #     "APN": "APN",
        #     "Owner 1 First Name":"Owner 1 First Name",
        #     "Owner 1 Last Name":"Owner 1 Last Name",
        #     "Owner 2 First Name": "Owner 2 First Name",
        #     "Owner 2 Last Name": "Owner 2 Last Name",
        #     "Mailing Address": "Mailing Address",
        #     "Mailing City": "Mailing City",
        #     "Property Type": "Property Type",
        #     "Building Sqft":"Building Sqft",
        #     "Bedrooms": "Bedrooms",
        #     "Total Bathrooms": "Total Bathrooms",
        #     "Bathrooms": "Bathrooms",
        #     "Lot Size Sqft": "Lot Size Sqft",
        #     "Year Built": "Year Built",
        #     "Occupancy": "Vacant",
        #     "Tax Assessed Value": "Total Assessed Value",
        #     "Date of Sale": "Last Sale Date",
        #     "Record Date": "Last Sale Recording Date",
        #     "Buyer Name": "Last Sale Buyer Name 1",
        #     "Loan 1 Balance": "Loan 1 Balance",
        #     "Loan 1 Type": "Loan 1 Type",
        #     "Loan 1 Rate": "Loan 1 Rate",
        #     "Loan 1 Rate Type": "Loan 1 Rate Type",
        #     "Loan 2 Balance": "Loan 2 Balance",
        #     "Loan 2 Type": "Loan 2 Type",
        #     "Loan 2 Rate": "Loan 2 Rate",
        #     "Loan 2 Rate Type": "Loan 2 Rate Type",
        #     "Value": "Est. Value",
        #     "Is there an HOA?":"HOA Present",
        #     "Loan To Value Ratio": "Est. Loan-to-Value",
        #     "Condition": "Total Condition",
        #     "Foreclosure Status": "Foreclosure Factor",
        #     "MLS Amount": "MLS Amount",
        #     "MLS Agent Name": "MLS Agent Name",
        #     "MLS Agent Phone": "MLS Agent Phone",
        #     "MLS Brokerage Name": "MLS Brokerage Name",
        #     "MLS Brokerage Phone": "MLS Brokerage Phone",
        #     "Lead Status": "Lead Status"
        # }

        crm_config = tenant.get("crm", {})
        map_data = crm_config.get("mapping", {})
        tags = crm_config.get("tags", [])
        username = crm_config.get("username", DEFAULT_USERNAME)
        webhook_url = crm_config.get("webhook_url", CRM_WEBHOOK_URL)
        tenant_id = tenant.get("id")

        current_datetime = datetime.now()
        date_tag = f"{current_datetime.strftime('%m/%d/%y')}"
        if date_tag not in tags:
            tags = tags + [date_tag]


        # Clear Sky Builder Mapping playload
        # map_data ={
        #     "first_name":"MLS Agent Name",
        #     "last_name":"MLS Agent Name",
        #     "phone_number":"MLS Agent Phone",
        #     "email":"MLS Agent E-Mail",
        #     "Property Address":"Address",
        #     "Property City":"City",
        #     "Property State":"State",
        #     "Property Zip":"Zip",
        #     "Property County":"County",
        #     "APN":"APN",
        #     "Owner 1 First Name":"Owner 1 First Name",
        #     "Owner 1 Last Name":"Owner 1 Last Name",
        #     "Owner 2 First Name":"Owner 2 First Name",
        #     "Owner 2 Last Name":"Owner 2 Last Name",
        #     "Property Type":"Property Type",
        #     "Bedrooms":"Bedrooms",
        #     "Bathrooms":"Total Bathrooms",
        #     "Building SqFt":"Building Sqft",
        #     "Lot Size Sqft":"Lot Size Sqft",
        #     "Year Built":"Year Built",
        #     "Is there an HOA?":"HOA Present",
        #     "Loan 1 Balance":"Loan 1 Balance",
        #     "Loan 1 Type":"Loan 1 Type",
        #     "Loan 1 Rate":"Loan 1 Rate",
        #     "Loan 1 Rate Type":"Loan 1 Rate Type",
        #     "Loan 2 Balance":"Loan 2 Balance",
        #     "Loan 2 Type":"Loan 2 Type",
        #     "Loan 2 Rate":"Loan 2 Rate",
        #     "Loan 2 Rate Type":"Loan 2 Rate Type",
        #     "Loan To Value Ratio":"Est. Loan-to-Value",
        #     "Actual Equity Value":"Est. Equity",
        #     "Condition":"Total Condition",
        #     "MLS Amount":"MLS Amount",
        #     "MLS Agent Name":"MLS Agent Name",
        #     "MLS Agent Phone":"MLS Agent Phone",
        #     "MLS Agent E-Mail":"MLS Agent E-Mail",
        #     "MLS Brokerage Name":"MLS Brokerage Name"
        # }
        
        files = {
            "new_members_file": (f"{datetime.now().strftime('%Y-%m-%d')}_padsplit_low_equity.csv", csv_file, "text/csv")
        }
        data_payload = {
            "map_data": json.dumps(map_data),
            "username": username,
            "tags": json.dumps(tags)
        }

        # 4️ Send POST request
        response = requests.post(
            f"{webhook_url}?tenant_id={tenant_id}",
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
