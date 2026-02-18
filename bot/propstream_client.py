import os
from datetime import datetime
import requests
from bot.config import TOKEN_FILE, LOGIN_URL, USERNAME, PASSWORD, HEADLESS
from bot.logger import setup_logger
from bot.token_manager import get_token

logger = setup_logger()

def read_token(token_file=TOKEN_FILE):
    if os.path.exists(token_file):
        with open(token_file) as f:
            return f.read().strip()
    logger.warning("Token file not found.")
    return None

def add_to_marketing_list(filters, token=None, file_name=f'{datetime.now().strftime("%Y-%m-%d")}_padsplit_low_equity'):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://app.propstream.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://app.propstream.com/search',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'x-auth-token': token if token else read_token(),
    }

    params = {
        'groupType': 'MARKETING',
        'groupName': file_name,
    }

    if not filters:
        logger.warning("No filters provided for marketing list creation.")
        return

    for index, item in enumerate(filters, start=1):
        payload = item.get("payload", item)
        response = requests.post(
            'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
            params=params,
            headers=headers,
            json=payload,
        )
        logger.info(f"Add to marketing list response {index} status: {response.status_code}")



def get_marketingList_Id(token=None, token_file=TOKEN_FILE, fileName=f'{datetime.now().strftime("%Y-%m-%d")}_padsplit_low_equity'):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://app.propstream.com/property/group/4993672',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'x-auth-token': token if token else read_token(token_file),
    }

    response = requests.get(
        'https://app.propstream.com/eqbackend/resource/auth?t&c&overtake=false&dev=false',
        headers=headers,
    )

    if response.status_code == 200:
        logger.info("Successfully fetched All marketing lists.")
        data = response.json()

        TodayList = [item for item in data.get("propertyGroups", []) if item.get("name") == fileName]

        if TodayList:
            ListId = TodayList[0]["id"]
            logger.info(f"Found today's marketing list ID: {ListId}")
        else:
            logger.warning("Today's marketing list not found.")
            ListId = None
        
        return ListId
    elif response.status_code == 403:
        logger.error("Token expired or invalid (403). Consider refreshing it.")
        return None
    else:
        logger.error(f"Error fetching marketing list ID ({response.status_code}): {response.text}")
        return None

def fetch_properties(tenant):
    propstream = tenant.get("propstream", {})
    login_url = propstream.get("login_url", LOGIN_URL)
    username = propstream.get("username", USERNAME)
    password = propstream.get("password", PASSWORD)
    headless = propstream.get("headless", HEADLESS)
    token_file = propstream.get("token_file", TOKEN_FILE)
    filters = propstream.get("filters", [])
    list_prefix = propstream.get("list_name_prefix", "padsplit_low_equity")

    if not username or not password:
        logger.error("Missing PropStream credentials for tenant.")
        return None

    get_token(login_url=login_url, username=username, password=password, headless=headless, token_file=token_file)
    token = read_token(token_file)
    if not token:
        logger.error("❌ Missing token. Run token_manager.get_token() first.")
        # Send a information to the admin about missing token. using webhook.
        return None

    # Find the Marketing list [<today's date>_padsplit_low_equity] to extract the Id
    file_name = f"{datetime.now().strftime('%Y-%m-%d')}_{list_prefix}"
    ListId = get_marketingList_Id(token=token, token_file=token_file, fileName=file_name)
    if not ListId:
        logger.error("❌ Could not retrieve marketing list ID.")

        # If there is no the list then create a new marketing list using add_to_marketing_list()
        logger.info("Creating a today's marketing list...")
        add_to_marketing_list(filters=filters, token=token, file_name=file_name)
        ListId = get_marketingList_Id(token=token, token_file=token_file, fileName=file_name)
        if not ListId:
            logger.error("❌ Marketing list ID still missing after creation attempt.")
            return None

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://app.propstream.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': f'https://app.propstream.com/property/group/{ListId}',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'x-auth-token': token if token else read_token(token_file),
    }

    params = {
        'refreshFilters': '0',
    }

    json_data = {
        'id': ListId,
        'name': 'Test_New_Bot_List',
        'filters': [],
        'sortModel': [],
        'allSelected': False,
        'remainingSelected': False,
        'selected': 0,
        'automationStatus': None,
        'valueCols': [
            {
                'colId': 'streetAddress',
                'headerName': 'Address',
            },
            {
                'colId': 'unitNumber',
                'headerName': 'Unit #',
            },
            {
                'colId': 'cityName',
                'headerName': 'City',
            },
            {
                'colId': 'stateCode',
                'headerName': 'State',
            },
            {
                'colId': 'zip',
                'headerName': 'Zip',
            },
            {
                'colId': 'plusFour',
                'headerName': 'Zip+4',
            },
            {
                'colId': 'carrierRoute',
                'headerName': 'Carrier Route',
            },
            {
                'colId': 'countyName',
                'headerName': 'County',
            },
            {
                'colId': 'fips',
                'headerName': 'FIPS',
            },
            {
                'colId': 'apn',
                'headerName': 'APN',
            },
            {
                'colId': 'ownerOccupied',
                'headerName': 'Owner Occupied',
            },
            {
                'colId': 'owner1FirstName',
                'headerName': 'Owner 1 First Name',
            },
            {
                'colId': 'owner1LastName',
                'headerName': 'Owner 1 Last Name',
            },
            {
                'colId': 'owner2FirstName',
                'headerName': 'Owner 2 First Name',
            },
            {
                'colId': 'owner2LastName',
                'headerName': 'Owner 2 Last Name',
            },
            {
                'colId': 'mailCareOf',
                'headerName': 'Mailing Care of Name',
            },
            {
                'colId': 'mailStreetAddress',
                'headerName': 'Mailing Address',
            },
            {
                'colId': 'mailUnitNumber',
                'headerName': 'Mailing Unit #',
            },
            {
                'colId': 'mailCityName',
                'headerName': 'Mailing City',
            },
            {
                'colId': 'mailStateCode',
                'headerName': 'Mailing State',
            },
            {
                'colId': 'mailZip',
                'headerName': 'Mailing Zip',
            },
            {
                'colId': 'mailPlusFour',
                'headerName': 'Mailing Zip+4',
            },
            {
                'colId': 'mailCarrierRoute',
                'headerName': 'Mailing Carrier Route',
            },
            {
                'colId': 'mailCountyName',
                'headerName': 'Mailing County',
            },
            {
                'colId': 'mailFips',
                'headerName': 'Mailing FIPS',
            },
            {
                'colId': 'mailOptOut',
                'headerName': 'Do Not Mail',
            },
            {
                'colId': 'decedent',
                'headerName': 'Deceased Owner',
            },
            {
                'colId': 'propertyClass',
                'headerName': 'Property Class',
            },
            {
                'colId': 'landUse',
                'headerName': 'Property Type',
            },
            {
                'colId': 'bedrooms',
                'headerName': 'Bedrooms',
            },
            {
                'colId': 'bathrooms',
                'headerName': 'Total Bathrooms',
            },
            {
                'colId': 'squareFeet',
                'headerName': 'Building Sqft',
            },
            {
                'colId': 'lotSquareFeet',
                'headerName': 'Lot Size Sqft',
            },
            {
                'colId': 'yearBuilt',
                'headerName': 'Year Built',
            },
            {
                'colId': 'effectiveYearBuilt',
                'headerName': 'Effective Year Built',
            },
            {
                'colId': 'poolType',
                'headerName': 'Pool Type',
            },
            {
                'colId': 'vacant',
                'headerName': 'Vacant',
            },
            {
                'colId': 'hoaPresent',
                'headerName': 'HOA Present',
            },
            {
                'colId': 'stories',
                'headerName': 'Number of Stories',
            },
            {
                'colId': 'assessedValue',
                'headerName': 'Total Assessed Value',
            },
            {
                'colId': 'assessedLandValue',
                'headerName': 'Assessed Land Value',
            },
            {
                'colId': 'assessedImprovementValue',
                'headerName': 'Assessed Improvement Value',
            },
            {
                'colId': 'itvRatio',
                'headerName': 'Improvement to Tax Value %',
            },
            {
                'colId': 'lastSaleDate',
                'headerName': 'Last Sale Date',
            },
            {
                'colId': 'lastRecordingDate',
                'headerName': 'Last Sale Recording Date',
            },
            {
                'colId': 'lastSaleAmount',
                'headerName': 'Last Sale Amount',
            },
            {
                'colId': 'cashBuyer',
                'headerName': 'Last Cash Buyer',
            },
            {
                'colId': 'lastOwner1Name',
                'headerName': 'Last Sale Buyer Name 1',
            },
            {
                'colId': 'lastOwner2Name',
                'headerName': 'Last Sale Buyer Name 2',
            },
            {
                'colId': 'priorSaleDate',
                'headerName': 'Prior Sale Date',
            },
            {
                'colId': 'priorRecordingDate',
                'headerName': 'Prior Sale Recordng Date',
            },
            {
                'colId': 'priorSaleAmount',
                'headerName': 'Prior Sale Amount',
            },
            {
                'colId': 'priorCashSale',
                'headerName': 'Prior Sale Cash Buyer',
            },
            {
                'colId': 'priorOwner1Name',
                'headerName': 'Prior Sale Buyer Name 1',
            },
            {
                'colId': 'priorOwner2Name',
                'headerName': 'Prior Sale Buyer Name 2',
            },
            {
                'colId': 'mortgage1RecordingDate',
                'headerName': 'Loan 1 Date',
            },
            {
                'colId': 'mortgage1Balance',
                'headerName': 'Loan 1 Balance',
            },
            {
                'colId': 'mortgage1LoanType',
                'headerName': 'Loan 1 Type',
            },
            {
                'colId': 'mortgage1LenderName',
                'headerName': 'Loan 1 Lender',
            },
            {
                'colId': 'mortgage1InterestRate',
                'headerName': 'Loan 1 Rate',
            },
            {
                'colId': 'mortgage1FinancingType',
                'headerName': 'Loan 1 Rate Type',
            },
            {
                'colId': 'mortgage2RecordingDate',
                'headerName': 'Loan 2 Date',
            },
            {
                'colId': 'mortgage2Balance',
                'headerName': 'Loan 2 Balance',
            },
            {
                'colId': 'mortgage2LoanType',
                'headerName': 'Loan 2 Type',
            },
            {
                'colId': 'mortgage2LenderName',
                'headerName': 'Loan 2 Lender',
            },
            {
                'colId': 'mortgage2InterestRate',
                'headerName': 'Loan 2 Rate',
            },
            {
                'colId': 'mortgage2FinancingType',
                'headerName': 'Loan 2 Rate Type',
            },
            {
                'colId': 'mortgage3RecordingDate',
                'headerName': 'Loan 3 Date',
            },
            {
                'colId': 'mortgage3Balance',
                'headerName': 'Loan 3 Balance',
            },
            {
                'colId': 'mortgage3LoanType',
                'headerName': 'Loan 3 Type',
            },
            {
                'colId': 'mortgage3LenderName',
                'headerName': 'Loan 3 Lender',
            },
            {
                'colId': 'mortgage3InterestRate',
                'headerName': 'Loan 3 Rate',
            },
            {
                'colId': 'mortgage3FinancingType',
                'headerName': 'Loan 3 Rate Type',
            },
            {
                'colId': 'mortgage4RecordingDate',
                'headerName': 'Loan 4 Date',
            },
            {
                'colId': 'mortgage4Balance',
                'headerName': 'Loan 4 Balance',
            },
            {
                'colId': 'mortgage4LoanType',
                'headerName': 'Loan 4 Type',
            },
            {
                'colId': 'mortgage4LenderName',
                'headerName': 'Loan 4 Lender',
            },
            {
                'colId': 'mortgage4InterestRate',
                'headerName': 'Loan 4 Rate',
            },
            {
                'colId': 'mortgage4FinancingType',
                'headerName': 'Loan 4 Rate Type',
            },
            {
                'colId': 'openMortgageQuantity',
                'headerName': 'Total Open Loans',
            },
            {
                'colId': 'openMortgageBalance',
                'headerName': 'Est. Remaining balance of Open Loans',
            },
            {
                'colId': 'estimatedValue',
                'headerName': 'Est. Value',
            },
            {
                'colId': 'ltvRatio',
                'headerName': 'Est. Loan-to-Value',
            },
            {
                'colId': 'estimatedEquity',
                'headerName': 'Est. Equity',
            },
            {
                'colId': 'rentAmount',
                'headerName': 'Monthly Rent',
            },
            {
                'colId': 'grossYield',
                'headerName': 'Gross Yield %',
            },
            {
                'colId': 'mortgageTotalPayment',
                'headerName': 'Est. Total Monthly Payments',
            },
            {
                'colId': 'propcondition',
                'headerName': 'Total Condition',
            },
            {
                'colId': 'interior',
                'headerName': 'Interior Condition',
            },
            {
                'colId': 'exterior',
                'headerName': 'Exterior Condition',
            },
            {
                'colId': 'bathroom',
                'headerName': 'Bathroom Condition',
            },
            {
                'colId': 'kitchen',
                'headerName': 'Kitchen Condition',
            },
            {
                'colId': 'foreclosurefactorscore',
                'headerName': 'Foreclosure Factor',
            },
            {
                'colId': 'mlsStatus',
                'headerName': 'MLS Status',
            },
            {
                'colId': 'mlsListingDate',
                'headerName': 'MLS Date',
            },
            {
                'colId': 'mlsListingAmount',
                'headerName': 'MLS Amount',
            },
            {
                'colId': 'mlsAgentName',
                'headerName': 'MLS Agent Name',
            },
            {
                'colId': 'mlsAgentPhone',
                'headerName': 'MLS Agent Phone',
            },
            {
                'colId': 'mlsAgentEmail',
                'headerName': 'MLS Agent E-Mail',
            },
            {
                'colId': 'mlsOfficeName',
                'headerName': 'MLS Brokerage Name',
            },
            {
                'colId': 'mlsOfficePhone',
                'headerName': 'MLS Brokerage Phone',
            },
            {
                'colId': 'lienDocumentType',
                'headerName': 'Lien Type',
            },
            {
                'colId': 'lienRecordingDate',
                'headerName': 'Lien Date',
            },
            {
                'colId': 'lienListingAmount',
                'headerName': 'Lien Amount',
            },
            {
                'colId': 'bankruptcyRecordingDate',
                'headerName': 'BK Date',
            },
            {
                'colId': 'divorceRecordingDate',
                'headerName': 'Divorce Date',
            },
            {
                'colId': 'pfcRecordingDate',
                'headerName': 'Pre-FC Recording Date',
            },
            {
                'colId': 'pfcDocumentType',
                'headerName': 'Pre-FC Record Type',
            },
            {
                'colId': 'pfcLenderName',
                'headerName': 'Pre-FC Lender',
            },
            {
                'colId': 'pfcDocumentNumber',
                'headerName': 'Pre-FC Doc Number',
            },
            {
                'colId': 'pfcUnpaidBalance',
                'headerName': 'Pre-FC Unpaid Balance',
            },
            {
                'colId': 'pfcDefaultAmount',
                'headerName': 'Pre-FC Default Amount',
            },
            {
                'colId': 'pfcAuctionDate',
                'headerName': 'Pre-FC Auction Date',
            },
            {
                'colId': 'pfcAuctionTime',
                'headerName': 'Pre-FC Auction Time',
            },
            {
                'colId': 'pfcAuctionAddress',
                'headerName': 'Pre-FC Auction Location',
            },
            {
                'colId': 'pfcAuctionOpeningBid',
                'headerName': 'Pre-FC Auction Opening Bid',
            },
            {
                'colId': 'pfcTrusteeName',
                'headerName': 'Pre-FC Trustee-Attorney Name',
            },
            {
                'colId': 'pfcTrusteeReferenceNumber',
                'headerName': 'Pre-FC Trustee Ref Number',
            },
            {
                'colId': 'pfcCaseNumber',
                'headerName': 'Pre-FC Attorney Case Number',
            },
            {
                'colId': 'pfcTrusteeAddress',
                'headerName': 'Pre-FC Trustee-Attorney Address',
            },
            {
                'colId': 'pfcBorrower1Name',
                'headerName': 'Pre-FC Borrower 1 Name',
            },
            {
                'colId': 'addDate',
                'headerName': 'Date Added to List',
            },
            {
                'colId': 'addMethod',
                'headerName': 'Method of Add',
            },
        ],
        'selectedIds': [],
        'unselectedIds': [],
        'startRow': 0,
        'endRow': 500,
    }

    logger.info("Fetching property data from PropStream API...")
    try:
        response = requests.post("https://app.propstream.com/eqbackend/resource/auth/ps4/user/properties", headers=headers, json=json_data, params=params)
        if response.status_code == 200:
            data = response.json()
            data["mapping_data"] = json_data
            return data
        elif response.status_code == 403:
            logger.error("Token expired or invalid (403). Consider refreshing it.")
        else:
            logger.error(f"Error fetching data ({response.status_code}): {response.text}")
    except Exception as e:
        logger.exception(f"Error fetching property data: {e}")

    return None
