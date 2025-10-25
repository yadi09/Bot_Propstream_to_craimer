import os
import json
import requests
from datetime import datetime
from bot.config import BASE_API_URL, DATA_DIR, TOKEN_FILE
from bot.logger import setup_logger

logger = setup_logger("propstream_client")

def read_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return f.read().strip()
    logger.warning("Token file not found.")
    return None

def fetch_properties():
    os.makedirs(DATA_DIR, exist_ok=True)
    token = read_token()
    if not token:
        logger.error("❌ Missing token. Run token_manager.get_token() first.")
        return None

    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0',
        'x-auth-token': token,
    }

    params = {
        'refreshFilters': 'false',
    }

    json_data = {
        'id': 1,
        'name': 'All Automated Properties',
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
        'startRow': 0,
        'endRow': 500,
    }


    logger.info("Fetching property data from PropStream API...")
    try:
        response = requests.post(BASE_API_URL, headers=headers, json=json_data, params=params)
        if response.status_code == 200:
            data = response.json()
            data["mapping_data"] = json_data
            filename = f"{DATA_DIR}/properties_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            logger.info(f"✅ Data saved locally to {filename}")
            return data
        elif response.status_code == 403:
            logger.error("Token expired or invalid (403). Consider refreshing it.")
        else:
            logger.error(f"Error fetching data ({response.status_code}): {response.text}")
    except Exception as e:
        logger.exception(f"Error fetching property data: {e}")

    return None
