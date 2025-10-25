import multiprocessing
import uvicorn
from bot.scheduler import start_scheduler
from bot.logger import setup_logger

logger = setup_logger("main")

def run_api():
    """Run FastAPI server in a separate process"""
    logger.info("Starting FastAPI API server...")
    uvicorn.run("bot.api:app", host="0.0.0.0", port=8000, reload=False)

def run_scheduler():
    """Run the background scheduler"""
    logger.info("Starting scheduler service...")
    start_scheduler()

if __name__ == "__main__":
    logger.info("🚀 Starting PropStream Automation (API + Scheduler)...")

    # Create two separate processes
    api_process = multiprocessing.Process(target=run_api)
    scheduler_process = multiprocessing.Process(target=run_scheduler)

    # Start both
    api_process.start()
    scheduler_process.start()

    logger.info("✅ Both API and Scheduler started successfully.")

    # Wait for both processes to finish (block main thread)
    api_process.join()
    scheduler_process.join()
