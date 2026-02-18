import os
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bot.config import LOGIN_URL, USERNAME, PASSWORD, HEADLESS, TOKEN_FILE
from bot.logger import setup_logger

logger = setup_logger()

MAX_RETRIES = 5       # Number of times to retry the whole process
RETRY_DELAY = 5      # Delay in seconds between retries

def get_token(
    login_url=LOGIN_URL,
    username=USERNAME,
    password=PASSWORD,
    headless=HEADLESS,
    token_file=TOKEN_FILE,
):
    for attempt in range(1, MAX_RETRIES + 1):
        logger.info(f"Attempt {attempt}/{MAX_RETRIES} to retrieve PropStream token...")
        token = None

        try:
            with sync_playwright() as p:
                try:
                    browser = p.chromium.launch(headless=headless, slow_mo=100)
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
                    page.goto(login_url, wait_until="domcontentloaded", timeout=60000)

                    logger.info("Filling login form...")
                    page.fill('input[type="text"], input[name="username"], input[type="email"]', username)
                    page.fill('input[type="password"]', password)
                    page.keyboard.press("Enter")

                    logger.info("Waiting for login to complete...")
                    page.wait_for_load_state("networkidle", timeout=600000)

                    # Retry loop for token capture
                    for i in range(6):
                        if token:
                            break
                        logger.info(f"Waiting for token... Attempt {i+1}/6")
                        page.wait_for_timeout(10000)
                        try:
                            page.reload(wait_until="networkidle")
                        except PlaywrightTimeoutError:
                            logger.warning("⚠️ Page reload timed out; retrying...")

                except Exception as e:
                    logger.exception(f"Unexpected Playwright error: {e}")
                    token = None
                finally:
                    try:
                        browser.close()
                    except Exception as e:
                        logger.warning(f"⚠️ Error closing browser: {e}")

        except Exception as e:
            logger.exception(f"Playwright launch failed: {e}")
            token = None

        if token:
            try:
                token_dir = os.path.dirname(token_file)
                if token_dir:
                    os.makedirs(token_dir, exist_ok=True)
                with open(token_file, "w") as f:
                    f.write(token)
                logger.info(f"Token saved to {token_file}")
            except Exception as e:
                logger.error(f"❌ Failed to write token file: {e}")
            return token
        else:
            logger.warning(f"❌ Token not found. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)

    logger.error("❌ All attempts to get the token failed.")
    return None
