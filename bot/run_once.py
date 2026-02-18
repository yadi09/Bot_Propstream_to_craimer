from bot.logger import setup_logger
from bot.jobs import run_all_enabled_tenants

logger = setup_logger()

if __name__ == "__main__":
    logger.info("Starting one-off run for all enabled tenants...")
    run_all_enabled_tenants()
    logger.info("One-off run complete.")
