import schedule
import time
from bot.propstream_client import fetch_properties
from bot.crm_client import send_to_crm
from bot.logger import setup_logger
from bot.token_manager import get_token


logger = setup_logger()

def job():
    logger.info("--> Starting scheduled fetch job...")
    data = fetch_properties()
    if not data:
        logger.warning("No data fetched, refreshing token and retrying...")
        get_token()
        data = fetch_properties()
        return
    if data:
        logger.info(f"Fetched {len(data.get('properties', []))} properties.")
        send_to_crm(data, tenant_id="1d8086e9-eb18-40f5-b2de-9075fdf236b9")

def start_scheduler():
    # schedule.every(1).minutes.do(job)
    schedule.every().sunday.at("10:00").do(job)
    logger.info(f"Scheduler started [runs every Sunday at 10:00].")
    job()  # Run immediately once
    while True:
        schedule.run_pending()
        logger.info("Waiting for the next scheduled job...")
        time.sleep(60) # Sleep for 60 seconds
        logger.info("Woke up to check for scheduled jobs.")
