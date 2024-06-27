# warwick-washer-api
Building the API that WashCo didn't :(

## Background
At the University of Warwick, the washing and drying services are outsourced to an external provider called WashCo. They provide a website to check the status of a cycle (availability, time remaining, etc) however the website is quite dated, unintuitive, and sometimes doesn't even load. The aim of this project is to design and implement an API wrapper which ultimately cleanses some data which we currently have access to. This can then be used to perhaps design a mobile application, or new web app which displays the data in a cleaner, more user friendly and less obfuscated format. If you are interested in seeing the current website, you can find it [here](https://www.washpoint.uk/location/university-of-warwick/).

## Existing API?
Currently the website seems to be pulling data in real time from some form of data source. To find this source, open `Developer Tools` on Safari and navigate to the `Network` section. A simple page refresh reveals some form of API of return type JSON. You can find an example reponse in the file [tocilResponse.json](/json/tocilResponse.json). The next steps are to copy the cURL of this request to implement it in Python. My tool of choice is [curlconverter](https://curlconverter.com/python/), and the template it provided was the following:
```python
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
```
If we run this and print the response, we get the expected JSON!

### Cleansing the request
After some trial and error, I found that all of the parameters used in the header but `'alliancels-organization-id'` are useless. Therefore the code can be simply reduced to the following:
```python
import requests

headers = {
    'alliancels-organization-id': '652210',
}

response = requests.get('https://api.alliancelslabs.com/washAlert/machines/7907', headers=headers)
```

This request is specific to Tocil. For our final API, we would like to be able to pass some short form alias and get a room-specific response. The numbering or rooms is rather unintuitive, so I manually found each room number from the original websites URLs. These can be found in the following table:

|                        | Westwood Arden | Westwood Bericote | Westwood Compton | Westwood Dunsmere | Westwood Emscote | Westwood Feldon | Westwood Gosford | Westwood Hampton | Westwood Kinghtcote | Westwood Loxley | Arthur Vick 1 | Arthur Vick 2 | Arthur Vick 3 | Benefactors 1 | Benefactors 2 | Bluebell 1 | Bluebell 2 | Bluebell 3 | Bluebell 4 | Claycroft 1 | Claycroft 2 | Claycroft 3 | Cryfield Village | Heronbank East | Heronbank West | International House | Jack Martin 3 | Lakeside 1 | Lakeside 4 | Sherbourne 1 | Sherbourne 5 | Sherbourne 7 | Tocil |
|------------------------|----------------|-------------------|------------------|-------------------|------------------|-----------------|------------------|------------------|---------------------|-----------------|---------------|---------------|---------------|---------------|---------------|------------|------------|------------|------------|-------------|-------------|-------------|-----------------|----------------|----------------|---------------------|---------------|------------|------------|--------------|--------------|--------------|-------|
| Alias                  | ww_arden       | ww_bericote       | ww_compton       | ww_dunsmere       | ww_emscote       | ww_feldon       | ww_gosford       | ww_hampton       | ww_kinghtcote       | ww_loxley       | av_1          | av_2          | av_3          | bf_1          | bf_2          | bb_1       | bb_2       | bb_3       | bb_4       | cc_1        | cc_2        | cc_3        | cryfield          | hb_east        | hb_west        | int_house           | jm_3          | ls_1       | ls_4       | sb_1         | sb_5         | sb_7         | tocil |
| Value                  | 7894           | 9269              | 9271             | 9267              | 9268             | 7896            | 9270             | 9276             | 9275                | 9273            | 9274          | 9272          | 9354          | 7900          | 7901          | 7903       | 9373       | 7904       | 7905       | 7908        | 7895        | 9353        | 9351             | 7899           | 9352           | 7902                | 7906          | 7897       | 7898       | 5982         | 5981         | 5983         | 7907  |

In the code, this is represented as the following dictionary:
```python
room_data = {"ww_arden": 7894, "ww_bericote": 9269, "ww_compton": 9271, "ww_dunsmere": 9267, "ww_emscote": 9268, "ww_feldon": 7896, "ww_gosford": 9270, "ww_hampton": 9276, "ww_kinghtcote": 9275, "ww_loxley": 9273, "av_1": 9274, "av_2": 9272, "av_3": 9354, "bf_1": 7900, "bf_2": 7901, "bb_1": 7903, "bb_2": 9373, "bb_3": 7904, "bb_4": 7905, "cc_1": 7908, "cc_2": 7895, "cc_3": 9353, "cryfield": 9351, "hb_east": 7899, "hb_west": 9352, "int_house": 7902, "jm_3": 7906, "ls_1": 7897, "ls_4": 7898, "sb_1": 5982, "sb_5": 5981, "sb_7": 5983, "tocil": 7907}
```
This allows for requests to be made in the following, simpler way:
```python
response = requests.get(f'https://api.alliancelslabs.com/washAlert/machines/{room_data[key]}', headers=headers)
```

## Cleansing the Response
If we take a look at the sample reponse from earlier ([tocilResponse.json](/json/tocilResponse.json)), it is clear that there are two main issues which we should address:
1. __Unnecessary additional data:__ We want to keep the API as simple as possible; there is no need to know the majority of the properties provided in the response such as `"serialNumber"` or `"controlId"`. Also the response contains information which we already know, for example the whole `"organization"` sub-object tells us the name of the university and the room identifier; these are parameters which we already know (we used them to make the request).
2. __Inconsistent formatting:__ The entire `"currentStatus"` property is formatted as a type string, however it's supposed to be JSON. (It even seems to have some sort of newline formatting as well).

To address both of these issues, I created an array with the names of all properties which are to be removed from the returned JSON. This array has variable name `attributes_to_remove` and there exists a similar array for the properties we don't need from `"currentStatus"` with variable name `current_status_attributes_to_remove`. Note that it is first neccessary to interpret `"currentStatus"` as JSON rather than text. This is done with the following snippet:
```python
json.loads(obj["currentStatus"])
```

### Keys with meaning
Up until now, we have gone over removing and interpreting properties within the response correctly. The next step is to place each object (machine) under a meaningful key. Logically, the key to use should be the machine number. This would help for future uses of this API wrapper in specific applications, say if you want to parse the JSON for a specific machine. To do this, we can use the following code:
```python
modified_data = {}

for obj in data:

    # relevant logic

    modified_data[int(machine_number)] = obj

modified_json_data = json.dumps(modified_data, indent=4)
```

This will mean that the JSON data is fromatted as follows:
```
{
  "12": {
    "machineNumber": 12,
    ...
  }
  ...
}
```
You can find a full-form example in the file [sampleCleansedTocilObject.json](/json/sampleCleansedTocilObject.json).

## Usage
To test out the wrapper yourself, clone the repository and run `main.py` ensuring to pass the room alias in `room_data[room_alias]}`. In my code, I have left Tocil as an example.

### Ideas
If you are interested in using this API, here are some ideas where you could apply it:
- Build a (better) web app to display the data
- Build an email/sms service to get machine availability
- Build an iOS app using Swift/SwiftUI to display the data (this is what I'm working on!)

### Flask Example
In case you want to host this API wrapper on a web server, check out the example of how I did it using flask. The code can be found in [flask-example.py](/flask-example.py).

An example call to an endpoint would look like `/washer?room=tocil&machine_number=1`. And the response, something like:
```JSON
{
   "currentStatus":{
      "isDoorOpen":false,
      "remainingSeconds":2120,
      "remainingVend":330,
      "selectedCycle":{
         "id":3,
         "name":"NORMAL_40C"
      },
      "statusId":"AVAILABLE"
   },
   "isActive":true,
   "machineNumber":1,
   "machineType":{
      "isDryer":false,
      "isWasher":true,
      "typeName":"Frontload Washer"
   }
}
```
