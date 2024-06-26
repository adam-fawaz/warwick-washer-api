# warwick-washer-api
Building the API that WashCo didn't :(

## Background
At the University of Warwick, the washing and drying services are outsourced to an external provider called WashCo. They provide a website to check the status of a cycle (availability, time remaining, etc) however the website is quite dated, unintuitive, and sometimes doesn't even load. The aim of this project is to design and implement an API wrapper which ultimately cleanses some data which we currently have access to. This can then be used to perhaps design a mobile application, or new web app which displays the data in a cleaner, more user friendly and less obfuscated format. If you are interested in seeing the current website, you can find it [here](https://www.washpoint.uk/location/university-of-warwick/).

## Existing API?
Currently the website seems to be pulling data in real time from some form of data source. To find this source, open `Developer Tools` on Safari and navigate to the `Sources` section. A simple page refresh reveals some form of API of return type JSON. You can find an example reponse in the file [tocilResponse.json](/json/tocilResponse.json). The next steps are to copy the cURL of this request and implement it in Python. My tool of choice is [curlconverter](https://curlconverter.com/python/), and the template it gave me was the following:
'''
import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Sec-Fetch-Site': 'cross-site',
    'Accept-Language': 'en-GB,en;q=0.9',
    # 'Accept-Encoding': 'gzip, deflate, br',
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
'''
