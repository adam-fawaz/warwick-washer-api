import requests
import json

# All the other parameters in the header are not needed
headers = {
    'alliancels-organization-id': '652210'
}

response = requests.get('https://api.alliancelslabs.com/washAlert/machines/7907', headers=headers)

data = response.json()
json_string = json.dumps(data, indent=4)
print(json_string)