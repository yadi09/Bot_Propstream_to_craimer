from playwright.sync_api import sync_playwright
from bot.config import LOGIN_URL, USERNAME, PASSWORD, HEADLESS, TOKEN_FILE
from bot.logger import setup_logger

logger = setup_logger()

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bot.config import LOGIN_URL, USERNAME, PASSWORD, HEADLESS, TOKEN_FILE
from bot.logger import setup_logger

logger = setup_logger()

def get_token():
    logger.info("Launching browser to retrieve PropStream token...")
    token = None

    try:
        with sync_playwright() as p:
            try:
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
                try:
                    page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=60000)
                except PlaywrightTimeoutError:
                    logger.error("❌ Page load timed out. Check LOGIN_URL or network connectivity.")
                    return None

                try:
                    page.fill('input[type="text"], input[name="username"], input[type="email"]', USERNAME)
                    page.fill('input[type="password"]', PASSWORD)
                    page.keyboard.press("Enter")
                except PlaywrightTimeoutError:
                    logger.error("❌ Form fields not found. Check if page layout changed.")
                    return None

                logger.info("Waiting for login to complete...")
                try:
                    page.wait_for_load_state("networkidle", timeout=150000)
                except PlaywrightTimeoutError:
                    logger.error("❌ Login process took too long or site failed to load.")
                    return None

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
                return None
            finally:
                try:
                    browser.close()
                except Exception as e:
                    logger.warning(f"⚠️ Error closing browser: {e}")

    except Exception as e:
        logger.exception(f"Playwright launch failed: {e}")
        return None

    if token:
        try:
            with open(TOKEN_FILE, "w") as f:
                f.write(token)
            logger.info(f"Token saved to {TOKEN_FILE}")
        except Exception as e:
            logger.error(f"❌ Failed to write token file: {e}")
    else:
        logger.error("❌ Token not found after login.")

    return token
