# warwick-washer-api
Building the API that WashCo didn't :(

## Background
At the University of Warwick, the washing and drying services are outsourced to an external provider called WashCo. They provide a website to check the status of a cycle (availability, time remaining, etc) however the website is quite dated, unintuitive, and sometimes doesn't even load. The aim of this project is to design and implement an API wrapper which ultimately cleanses some data which we currently have access to. This can then be used to perhaps design a mobile application, or new web app which displays the data in a cleaner, more user friendly and less obfuscated format. If you are interested in seeing the current website, you can find it [here](https://www.washpoint.uk/location/university-of-warwick/).

## Existing API?
Currently the website seems to be pulling data in real time from some form of data source. To find this source, open `Developer Tools` on Safari and navigate to the `Network` section. A simple page refresh reveals some form of API of return type JSON. You can find an example reponse in the file [tocilResponse.json](/json/tocilResponse.json). The next steps are to copy the cURL of this request to implement it in Python. My tool of choice is [curlconverter](https://curlconverter.com/python/), and the template it gave me was the following:
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
If we run this and print the response, we get the expected JSON response!

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




