import requests
import json

# All the other parameters in the header are not needed
headers = {
    'alliancels-organization-id': '652210'
}

response = requests.get('https://api.alliancelslabs.com/washAlert/machines/7907', headers=headers)

# Helper function to count the number occurences of a key
def count_key_occurrences(json_data, target_key):
    def recursive_count(data, target_key):
        count = 0
        if isinstance(data, dict):
            for key, value in data.items():
                if key == target_key:
                    count += 1
                count += recursive_count(value, target_key)
        elif isinstance(data, list):
            for item in data:
                count += recursive_count(item, target_key)
        return count

    return recursive_count(json_data, target_key)

data = response.json()
json_string = json.dumps(data, indent=4)
print(json_string)

target_name = 'currentStatus'
count = count_key_occurrences(data, target_name)
print(count)