from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import requests
from bot.logger import setup_logger
from bot.config import HEADLESS, LOGIN_URL, USERNAME, PASSWORD
import json
import time

logger = setup_logger()

MAX_RETRIES = 5      # Number of times to retry the whole process
RETRY_DELAY = 5      # Delay in seconds between retries
TARGET_URL = "https://app.propstream.com/eqbackend/resource/auth/ps4/property/comparables"
AUTH_TOKEN_HEADER = "x-auth-token"

def get_property_id(address: str) -> str:
    """
    Given an address, retrieve the property ID.
    """
    params = {
        'q': address,
    }

    response = requests.get(
        'https://app.propstream.com/eqbackend/resource/auth/ps4/property/suggestionsnew',
        params=params,
    )
    logger.info(f"✅ Requested property suggestions for address: {address}")

    if response.status_code == 200:
        data = response.json()
        if len(data) > 1 or len(data) == 0:
            logger.error(f"❌ Unexpected number of address found {address}: {len(data)}, please enter full address")
            return None
        return data[0]['id']
    

def get_filter_data(address_id: str) -> dict:
    """
    Given a property ID and token, retrieve filter data needed for comps.
    """
    # Further steps to get filter data and comps would go here
    logger.info(f"Starting process to get filter data for property ID: {address_id}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context()
        page = context.new_page()

        auth_token = None
        payload = None
        raw_data = None

        def on_request(request):
            """
            Callback function executed every time the browser initiates a request.
            This function checks if the request matches the target URL and extracts the data.
            """
            try:
                # 1. Filter the request by URL
                if TARGET_URL in request.url:
                    logger.info(f"\n--- Captured Request to: {request.url} ---")
                    
                    # 2. Extract the specific header (x-auth-token)
                    nonlocal auth_token
                    auth_token = request.headers.get(AUTH_TOKEN_HEADER, None)
                    if auth_token:
                        logger.info(f"Extracted {AUTH_TOKEN_HEADER}: {auth_token}")
                    else:
                        logger.warning(f"{AUTH_TOKEN_HEADER} not found in request headers.")

                    # 3. Extract the JSON Payload (Request Body)
                    try:
                        # Use post_data_json() for JSON bodies
                        nonlocal payload
                        payload = request.post_data_json
                        logger.info("Extracted Payload (JSON):")
                        # Print the payload nicely formatted
                        import json
                        logger.info(json.dumps(payload, indent=2))
                    except Exception:
                        # Fallback for non-JSON or missing bodies
                        nonlocal raw_data
                        raw_data = request.post_data
                        logger.info("Extracted Payload (Raw Text/Form Data):")
                        logger.info(raw_data)

            except Exception as e:
                # Catch any exceptions during data extraction
                logger.error(f"❌ Error extracting request data: {e}")

        page.on("request", on_request)

        logger.info("Navigating to login page...")
        page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=60000)

        logger.info("Filling login form...")
        page.fill('input[type="text"], input[name="username"], input[type="email"]', USERNAME)
        page.fill('input[type="password"]', PASSWORD)
        page.keyboard.press("Enter")

        logger.info("Waiting for login to complete...")

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                # Use a short timeout for each attempt (e.g., 10 seconds)
                page.wait_for_selector(
                    '.src-app-Search-Header-style__CXeKd__row', 
                    state='attached', 
                    timeout=10000
                )
                logger.info(f"✅ Selector found on attempt {attempt}.")
                break  # Exit the loop successfully
                
            except PlaywrightTimeoutError as e:
                if attempt < MAX_RETRIES:
                    logger.warning(f"⚠️ Selector not found (Attempt {attempt}/{MAX_RETRIES}). Retrying in {RETRY_DELAY}s...")
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error(f"❌ Login failed: Selector not found after {MAX_RETRIES} attempts. {e}")
                    # Raise the exception if the final attempt failed
                    raise

        logger.info("Starting navigation and element check process...")

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info(f"Attempt {attempt}/{MAX_RETRIES}: Navigating to URL...")
                
                # 1. ATTEMPT NAVIGATION (If this fails, the 'except' block handles the retry)
                if attempt == 1:
                    page.goto(
                        f"https://app.propstream.com/search/{address_id}", 
                        wait_until="domcontentloaded", 
                        timeout=60000  # 60 seconds for the initial page load
                    )
                
                # 2. WAIT FOR KEY ELEMENT (Shorter timeout, as page is mostly loaded)
                page.wait_for_selector(
                    '.react-tabs__tab', 
                    state='attached', 
                    timeout=60000 
                )
                
                logger.info(f"✅ Page loaded and selector found on attempt {attempt}.")
                break  # Success! Exit the loop
                
            except (PlaywrightTimeoutError, Exception) as e:
                if attempt < MAX_RETRIES:
                    logger.warning(f"⚠️ Navigation/Selector failure (Attempt {attempt}/{MAX_RETRIES}). Retrying in {RETRY_DELAY}s...")
                    time.sleep(RETRY_DELAY) # Pause before the next retry
                else:
                    logger.error(f"❌ Critical failure after {MAX_RETRIES} attempts. Cannot load page or find key element: {e}")
                    raise # Re-raise the exception to stop the script

        try:
            logger.info("Handling potential pop-up...")
            page.get_by_role("button", name="Proceed").click()
            logger.info("Pop-up closed.")
        except Exception as e:
            logger.info("No pop-up detected, continuing...")
            pass    

        logger.info("Clicking on 'Comparables & Nearby Listings' tab...")
        page.get_by_role("tab", name="Comparables & Nearby Listings").click()
        page.wait_for_load_state("networkidle", timeout=600000)

        logger.info("Waiting to capture the request data...")
        # Wait a bit to ensure the request is captured
        time.sleep(10)
        return { 'Token': auth_token, 'Payload': payload }


def get_comps_for_address(address: str):
    """
    Main function to get comps for a given address.
    """
    logger.info(f"Starting process to get comps for address: {address}")
    logger.info("Retrieving property ID...")
    address_id = get_property_id(address)
    if not address_id:
        logger.error(f"❌ Could not retrieve ID for address: {address}")
        return None
    logger.info(f"✅ Retrieved ID {address_id} for address: {address}")

    data = get_filter_data(address_id)
    # print(data)

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://app.propstream.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://app.propstream.com/search/1706793269',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'x-auth-token': data['Token'],
    }

    response = requests.post(
        'https://app.propstream.com/eqbackend/resource/auth/ps4/property/comparables',
        headers=headers,
        json=data['Payload'],
    )

    # save to json file
    # if response.status_code == 200:
    #     data = response.json()
    #     logger.info(f"✅ Retrieved {len(data)} comps for address: {address}")
    #     with open('z_comps_Data.json', 'w', encoding='utf-8') as f:
    #         f.write(json.dumps(data, ensure_ascii=False, indent=4))

    if response.status_code == 200:
        data = response.json()
        logger.info(f"✅ Retrieved {len(data)} comps for address: {address}")
        return data
    else:
        logger.error(f"❌ Failed to retrieve comps for address: {address}, Status Code: {response.status_code}")
        return None


# address = "1419 Alametos San Antonio, TX 78201"
# get_comps_for_address(address)