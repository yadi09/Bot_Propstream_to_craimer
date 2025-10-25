from playwright.sync_api import sync_playwright
import time
from bot.config import LOGIN_URL, USERNAME, PASSWORD, HEADLESS, TOKEN_FILE
from bot.logger import setup_logger

logger = setup_logger("token_manager")

def get_token():
    logger.info("Launching browser to retrieve PropStream token...")
    token = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, slow_mo=100)
        context = browser.new_context()
        page = context.new_page()

        def on_response(response):
            nonlocal token
            try:
                headers = response.request.headers
                if "x-auth-token" in headers and not token:
                    token = headers["x-auth-token"]
                    logger.info(f"[✅] Token captured from {response.url}")
            except Exception as e:
                logger.warning(f"Error reading headers: {e}")

        page.on("response", on_response)

        logger.info("Navigating to login page...")
        page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=60000)
        page.fill('input[type="text"], input[name="username"], input[type="email"]', USERNAME)
        page.fill('input[type="password"]', PASSWORD)
        page.keyboard.press("Enter")

        logger.info("Waiting for login to complete...")
        page.wait_for_load_state("networkidle", timeout=150000)

        for i in range(6):
            if token:
                break
            logger.info(f"Waiting for token... Attempt {i+1}/6")
            page.wait_for_timeout(10000)
            page.reload(wait_until="networkidle")

        browser.close()

    if token:
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
        logger.info(f"Token saved to {TOKEN_FILE}")
    else:
        logger.error("❌ Token not found after login.")
    return token
