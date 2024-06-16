import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Sec-Fetch-Site': 'cross-site',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Sec-Fetch-Mode': 'cors',
    'Host': 'api.alliancelslabs.com',
    'Origin': 'https://wa.sqinsights.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15',
    'Connection': 'keep-alive',
    'Referer': 'https://wa.sqinsights.com/',
    'Sec-Fetch-Dest': 'empty',
    'alliancels-organization-id': '652210',
}

response = requests.get('https://api.alliancelslabs.com/washAlert/machines/7907', headers=headers)