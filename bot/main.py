import uvicorn
from bot.logger import setup_logger

logger = setup_logger()

def run_api():
    """Run FastAPI server"""
    logger.info("Starting FastAPI API server...")
    uvicorn.run("bot.api:app", host="0.0.0.0")


if __name__ == "__main__":
    logger.info("🚀 Starting PropStream Automation API...")
    run_api()