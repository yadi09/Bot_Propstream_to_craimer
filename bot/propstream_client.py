import os
import requests
from datetime import datetime
from bot.config import TOKEN_FILE
from bot.logger import setup_logger
from bot.token_manager import get_token

logger = setup_logger()

def read_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return f.read().strip()
    logger.warning("Token file not found.")
    return None

def add_to_marketing_list(token=None, file_name=f'{datetime.now().strftime("%Y-%m-%d")}_padsplit_low_equity'):
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

    json_data_1 = {
        'estimatedEquityPercentMax': 0.2,
        'hoaPresent': False,
        'mlsListingStatus': 'ACTIVE,COMING_SOON',
        'rental': False,
        'mortgageTotalPaymentMax': 2000,
        'cityId': 42455,
        'squareFeetMin': 1500,
        'landUseCode': 'SFR',
        'mlsListingAmountMin': 60000,
        'bathroomsMin': 2,
        'propertyClassCode': 'R',
        'resultOffset': 1,
        'daysOnMarketMax': 300,
        'residentialPropCode': 'SFR',
        'type': None,
        'bedroomsMin': 3,
        'mlsListingAmountMax': 499000,
        'estimatedValueGrowthPeriod': 'ONE_MONTH',
        # 'resultLimit': 13,
        'selection': [],
        'selectionInversed': True,
    }

    json_data_2 = {
        'estimatedEquityPercentMax': 0.2,
        'hoaPresent': False,
        'mlsListingStatus': 'ACTIVE,COMING_SOON',
        'rental': False,
        'mortgageTotalPaymentMax': 2000,
        'cityId': 42455,
        'squareFeetMin': 1500,
        'landUseCode': 'SFR',
        'mlsListingAmountMin': 60000,
        'bathroomsMin': 2,
        'propertyClassCode': 'R',
        'resultOffset': 1,
        'mlsListingDateMin': 1757462400000,
        'residentialPropCode': 'SFR',
        'type': None,
        'bedroomsMin': 3,
        'mlsListingAmountMax': 499000,
        'estimatedValueGrowthPeriod': 'ONE_MONTH',
        # 'resultLimit': 6,
        'selection': [],
        'selectionInversed': True,
    }

    json_data_3 = {
        'estimatedEquityPercentMax': 0.2,
        'hoaPresent': False,
        'mlsListingStatus': 'ACTIVE,COMING_SOON',
        'rental': False,
        'countyId': 2378,
        'mortgageTotalPaymentMax': 2000,
        'squareFeetMin': 1500,
        'landUseCode': 'SFR',
        'mlsListingAmountMin': 60000,
        'bathroomsMin': 2,
        'propertyClassCode': 'R',
        'resultOffset': 1,
        'mlsListingDateMin': 1757462400000,
        'residentialPropCode': 'SFR',
        'type': None,
        'bedroomsMin': 3,
        'mlsListingAmountMax': 499000,
        'estimatedValueGrowthPeriod': 'ONE_MONTH',
        # 'resultLimit': 11,
        'selection': [],
        'selectionInversed': True,
    }

    json_data_4 = {
        'estimatedEquityPercentMax': 0.2,
        'hoaPresent': False,
        'mlsListingStatus': 'ACTIVE,COMING_SOON',
        'rental': False,
        'mortgageTotalPaymentMax': 2000,
        'cityId': 162245,
        'squareFeetMin': 1500,
        'landUseCode': 'SFR',
        'mlsListingAmountMin': 60000,
        'bathroomsMin': 2,
        'propertyClassCode': 'R',
        'resultOffset': 1,
        'daysOnMarketMax': 300,
        'residentialPropCode': 'SFR',
        'type': None,
        'bedroomsMin': 3,
        'mlsListingAmountMax': 499000,
        'estimatedValueGrowthPeriod': 'ONE_MONTH',
        'resultLimit': 19,
        'selection': [],
        'selectionInversed': True,
    }

    json_data_5 = {
        'estimatedEquityPercentMax': 0.2,
        'hoaPresent': False,
        'mlsListingStatus': 'ACTIVE,COMING_SOON',
        'rental': False,
        'mortgageTotalPaymentMax': 2000,
        'cityId': 168748,
        'squareFeetMin': 1500,
        'landUseCode': 'SFR',
        'mlsListingAmountMin': 60000,
        'bathroomsMin': 2,
        'propertyClassCode': 'R',
        'resultOffset': 1,
        'daysOnMarketMax': 300,
        'residentialPropCode': 'SFR',
        'type': None,
        'bedroomsMin': 3,
        'mlsListingAmountMax': 499000,
        'estimatedValueGrowthPeriod': 'ONE_MONTH',
        'resultLimit': 6,
        'selection': [],
        'selectionInversed': True,
    }

    json_data_6 = {
        'estimatedEquityPercentMax': 0.3,
        'mlsListingStatus': 'ACTIVE,COMING_SOON',
        'rental': False,
        'mortgageTotalPaymentMax': 2000,
        'cityId': 162654,
        'squareFeetMin': 2400,
        'landUseCode': 'SFR',
        'mlsListingAmountMin': 60000,
        'bathroomsMin': 2,
        'propertyClassCode': 'R',
        'resultOffset': 1,
        'mlsListingDateMin': 1735776000000,
        'residentialPropCode': 'SFR',
        'type': None,
        'bedroomsMin': 3,
        'mlsListingAmountMax': 499000,
        'estimatedValueGrowthPeriod': 'ONE_MONTH',
        'resultLimit': 8,
        'mortgageInterestRateMax': 0.05,
        'selection': [],
        'selectionInversed': True,
    }

    json_data_7 = {
        'estimatedEquityPercentMax': 0.2,
        'hoaPresent': False,
        'mlsListingStatus': 'ACTIVE,COMING_SOON',
        'rental': False,
        'mortgageTotalPaymentMax': 1900,
        'cityId': 164049,
        'squareFeetMin': 1500,
        'landUseCode': 'SFR',
        'mlsListingAmountMin': 60000,
        'bathroomsMin': 2,
        'propertyClassCode': 'R',
        'resultOffset': 1,
        'mlsListingDateMin': 1757462400000,
        'residentialPropCode': 'SFR',
        'type': None,
        'bedroomsMin': 3,
        'mlsListingAmountMax': 499000,
        'estimatedValueGrowthPeriod': 'ONE_MONTH',
        'resultLimit': 12,
        'selection': [],
        'selectionInversed': True,
    }

    json_data_8 = {
        'estimatedEquityPercentMax': 0.2,
        'hoaPresent': False,
        'mlsListingStatus': 'ACTIVE,COMING_SOON',
        'rental': False,
        'mortgageTotalPaymentMax': 2000,
        'cityId': 164049,
        'squareFeetMin': 1500,
        'landUseCode': 'SFR',
        'mlsListingAmountMin': 60000,
        'bathroomsMin': 2,
        'propertyClassCode': 'R',
        'resultOffset': 1,
        'daysOnMarketMax': 300,
        'residentialPropCode': 'SFR',
        'type': None,
        'bedroomsMin': 3,
        'mlsListingAmountMax': 499000,
        'estimatedValueGrowthPeriod': 'ONE_MONTH',
        'resultLimit': 40,
        'selection': [],
        'selectionInversed': True,
    }

    json_data_9 = {
        'estimatedEquityPercentMax': 0.2,
        'hoaPresent': False,
        'mlsListingStatus': 'ACTIVE,COMING_SOON',
        'rental': False,
        'mortgageTotalPaymentMax': 2000,
        'cityId': 96373,
        'squareFeetMin': 1500,
        'landUseCode': 'SFR',
        'mlsListingAmountMin': 60000,
        'bathroomsMin': 2,
        'propertyClassCode': 'R',
        'resultOffset': 1,
        'daysOnMarketMax': 300,
        'residentialPropCode': 'SFR',
        'type': None,
        'bedroomsMin': 3,
        'mlsListingAmountMax': 499000,
        'estimatedValueGrowthPeriod': 'ONE_MONTH',
        'resultLimit': 24,
        'selection': [],
        'selectionInversed': True,
    }

    json_data_10 = {
        'estimatedEquityPercentMax': 0.2,
        'hoaPresent': False,
        'mlsListingStatus': 'ACTIVE,COMING_SOON',
        'rental': False,
        'mortgageTotalPaymentMax': 2000,
        'cityId': 102609,
        'squareFeetMin': 1500,
        'landUseCode': 'SFR',
        'mlsListingAmountMin': 60000,
        'bathroomsMin': 2,
        'propertyClassCode': 'R',
        'resultOffset': 1,
        'daysOnMarketMax': 300,
        'residentialPropCode': 'SFR',
        'type': None,
        'bedroomsMin': 3,
        'mlsListingAmountMax': 499000,
        'estimatedValueGrowthPeriod': 'ONE_MONTH',
        'resultLimit': 6,
        'selection': [],
        'selectionInversed': True,
    }

    json_data_11 = {
        'estimatedEquityPercentMax': 0.2,
        'hoaPresent': False,
        'mlsListingStatus': 'ACTIVE,COMING_SOON',
        'rental': False,
        'countyId': 155,
        'mortgageTotalPaymentMax': 2500,
        'squareFeetMin': 1200,
        'landUseCode': 'SFR',
        'mlsListingAmountMin': 200000,
        'bathroomsMin': 2,
        'propertyClassCode': 'R',
        'resultOffset': 1,
        'daysOnMarketMax': 300,
        'residentialPropCode': 'SFR',
        'type': None,
        'bedroomsMin': 3,
        'mlsListingAmountMax': 600000,
        'estimatedValueGrowthPeriod': 'ONE_MONTH',
        'resultLimit': 95,
        'selection': [],
        'selectionInversed': True,
    }

    json_data_12 = {
        'estimatedEquityPercentMax': 0.2,
        'hoaPresent': False,
        'mlsListingStatus': 'ACTIVE,COMING_SOON',
        'rental': False,
        'mortgageTotalPaymentMax': 2000,
        'cityId': 69603,
        'squareFeetMin': 1500,
        'landUseCode': 'SFR',
        'mlsListingAmountMin': 60000,
        'bathroomsMin': 2,
        'propertyClassCode': 'R',
        'resultOffset': 1,
        'daysOnMarketMax': 300,
        'residentialPropCode': 'SFR',
        'type': None,
        'bedroomsMin': 3,
        'mlsListingAmountMax': 499000,
        'estimatedValueGrowthPeriod': 'ONE_MONTH',
        'resultLimit': 9,
        'selection': [],
        'selectionInversed': True,
    }

    json_data_13 = {
        'estimatedEquityPercentMax': 0.2,
        'hoaPresent': False,
        'mlsListingStatus': 'ACTIVE,COMING_SOON',
        'rental': False,
        'mortgageTotalPaymentMax': 2000,
        'cityId': 160901,
        'squareFeetMin': 1500,
        'landUseCode': 'SFR',
        'mlsListingAmountMin': 60000,
        'bathroomsMin': 2,
        'propertyClassCode': 'R',
        'resultOffset': 1,
        'daysOnMarketMax': 300,
        'residentialPropCode': 'SFR',
        'type': None,
        'bedroomsMin': 3,
        'mlsListingAmountMax': 499000,
        'estimatedValueGrowthPeriod': 'ONE_MONTH',
        'resultLimit': 49,
        'selection': [],
        'selectionInversed': True,
    }

    json_data_14 = {
        'estimatedEquityPercentMax': 0.2,
        'hoaPresent': False,
        'mlsListingStatus': 'ACTIVE,COMING_SOON',
        'rental': False,
        'mortgageTotalPaymentMax': 2000,
        'cityId': 61968,
        'squareFeetMin': 1500,
        'landUseCode': 'SFR',
        'mlsListingAmountMin': 60000,
        'bathroomsMin': 2,
        'propertyClassCode': 'R',
        'resultOffset': 1,
        'mlsListingDateMin': 1755043200000,
        'residentialPropCode': 'SFR',
        'type': None,
        'bedroomsMin': 3,
        'mlsListingAmountMax': 499000,
        'estimatedValueGrowthPeriod': 'ONE_MONTH',
        # 'resultLimit': 9,
        'selection': [],
        'selectionInversed': True,
    }

    json_data_15 = {
        'estimatedEquityPercentMax': 0.2,
        'hoaPresent': False,
        'mlsListingStatus': 'ACTIVE,COMING_SOON',
        'rental': False,
        'mortgageTotalPaymentMax': 2000,
        'cityId': 96373,
        'squareFeetMin': 1500,
        'landUseCode': 'SFR',
        'mlsListingAmountMin': 60000,
        'bathroomsMin': 2,
        'propertyClassCode': 'R',
        'resultOffset': 1,
        'mlsListingDateMin': 1755043200000,
        'residentialPropCode': 'SFR',
        'type': None,
        'bedroomsMin': 3,
        'mlsListingAmountMax': 499000,
        'estimatedValueGrowthPeriod': 'ONE_MONTH',
        # 'resultLimit': 25,
        'selection': [],
        'selectionInversed': True,
    }

    json_data_16 = {
        'estimatedEquityPercentMax': 0.2,
        'hoaPresent': False,
        'mlsListingStatus': 'ACTIVE,COMING_SOON',
        'rental': False,
        'mortgageTotalPaymentMax': 2000,
        'cityId': 61704,
        'squareFeetMin': 1500,
        'landUseCode': 'SFR',
        'mlsListingAmountMin': 60000,
        'bathroomsMin': 2,
        'propertyClassCode': 'R',
        'resultOffset': 1,
        'mlsListingDateMin': 1755043200000,
        'residentialPropCode': 'SFR',
        'type': None,
        'bedroomsMin': 3,
        'mlsListingAmountMax': 499000,
        'estimatedValueGrowthPeriod': 'ONE_MONTH',
        # 'resultLimit': 22,
        'selection': [],
        'selectionInversed': True,
    }

    # response_1 = requests.post(
    #     'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
    #     params=params,
    #     headers=headers,
    #     json=json_data_1,
    # )
    # logger.info(f"Add to marketing list response 1 status: {response_1.status_code}")
    
    # response_2 = requests.post(
    #     'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
    #     params=params,
    #     headers=headers,
    #     json=json_data_2,
    # )
    # logger.info(f"Add to marketing list response 2 status: {response_2.status_code}")
    
    # response_3 = requests.post(
    #     'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
    #     params=params,
    #     headers=headers,
    #     json=json_data_3,
    # )
    # logger.info(f"Add to marketing list response 3 status: {response_3.status_code}")
    
    # response_4 = requests.post(
    #     'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
    #     params=params,
    #     headers=headers,
    #     json=json_data_4,
    # )
    # logger.info(f"Add to marketing list response 4 status: {response_4.status_code}")
    
    # response_5 = requests.post(
    #     'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
    #     params=params,
    #     headers=headers,
    #     json=json_data_5,
    # )
    # logger.info(f"Add to marketing list response 5 status: {response_5.status_code}")
    
    # response_6 = requests.post(
    #     'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
    #     params=params,
    #     headers=headers,
    #     json=json_data_6,
    # )
    # logger.info(f"Add to marketing list response 6 status: {response_6.status_code}")
    
    # response_7 = requests.post(
    #     'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
    #     params=params,
    #     headers=headers,
    #     json=json_data_7,
    # )
    # logger.info(f"Add to marketing list response 7 status: {response_7.status_code}")
    
    # response_8 = requests.post(
    #     'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
    #     params=params,
    #     headers=headers,
    #     json=json_data_8,
    # )
    # logger.info(f"Add to marketing list response 8 status: {response_8.status_code}")
    
    # response_9 = requests.post(
    #     'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
    #     params=params,
    #     headers=headers,
    #     json=json_data_9,
    # )
    # logger.info(f"Add to marketing list response 9 status: {response_9.status_code}")
    
    # response_10 = requests.post(
    #     'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
    #     params=params,
    #     headers=headers,
    #     json=json_data_10,
    # )
    # logger.info(f"Add to marketing list response 10 status: {response_10.status_code}")
    
    # response_11 = requests.post(
    #     'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
    #     params=params,
    #     headers=headers,
    #     json=json_data_11,
    # )
    # logger.info(f"Add to marketing list response 11 status: {response_11.status_code}")
    
    # response_12 = requests.post(
    #     'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
    #     params=params,
    #     headers=headers,
    #     json=json_data_12,
    # )
    # logger.info(f"Add to marketing list response 12 status: {response_12.status_code}")
    
    # response_13 = requests.post(
    #     'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
    #     params=params,
    #     headers=headers,
    #     json=json_data_13,
    # )
    # logger.info(f"Add to marketing list response 13 status: {response_13.status_code}")

    response_14 = requests.post(
        'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
        params=params,
        headers=headers,
        json=json_data_14,
    )
    logger.info(f"Add to marketing list response 14 status: {response_14.status_code}")

    response_15 = requests.post(
        'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
        params=params,
        headers=headers,
        json=json_data_15,
    )
    logger.info(f"Add to marketing list response 15 status: {response_15.status_code}")

    response_16 = requests.post(
        'https://app.propstream.com/eqbackend/resource/auth/ps4/user/listings',
        params=params,
        headers=headers,
        json=json_data_16,
    )
    logger.info(f"Add to marketing list response 16 status: {response_16.status_code}")

def get_marketingList_Id(token=None, fileName=f'{datetime.now().strftime("%Y-%m-%d")}_padsplit_low_equity'):
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
        'x-auth-token': token if token else read_token(),
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

def fetch_properties():
    get_token()
    token = read_token()
    if not token:
        logger.error("❌ Missing token. Run token_manager.get_token() first.")
        # Send a information to the admin about missing token. using webhook.

    # Find the Marketing list [<today's date>_padsplit_low_equity] to extract the Id
    ListId = get_marketingList_Id(token)
    if not ListId:
        logger.error("❌ Could not retrieve marketing list ID.")

        # If there is no the list then create a new marketing list using add_to_marketing_list()
        logger.info("Creating a today's marketing list...")
        fileName = f"{datetime.now().strftime('%Y-%m-%d')}_padsplit_low_equity"
        add_to_marketing_list(token, fileName)
        ListId = get_marketingList_Id(token, fileName)

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
        'x-auth-token': token if token else read_token(),
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
