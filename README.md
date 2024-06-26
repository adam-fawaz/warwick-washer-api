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

|Room Name            | Alias         | Value |
|---------------------|---------------|-------|
| Westwood Arden      | ww_arden      | 7894  |
| Westwood Bericote   | ww_bericote   | 9269  |
| Westwood Compton    | ww_compton    | 9271  |
| Westwood Dunsmere   | ww_dunsmere   | 9267  |
| Westwood Emscote    | ww_emscote    | 9268  |
| Westwood Feldon     | ww_feldon     | 7896  |
| Westwood Gosford    | ww_gosford    | 9270  |
| Westwood Hampton    | ww_hampton    | 9276  |
| Westwood Kinghtcote | ww_kinghtcote | 9275  |
| Westwood Loxley     | ww_loxley     | 9273  |
| Arthur Vick 1       | av_1          | 9274  |
| Arthur Vick 2       | av_2          | 9272  |
| Arthur Vick 3       | av_3          | 9354  |
| Benefactors 1       | bf_1          | 7900  |
| Benefactors 2       | bf_2          | 7901  |
| Bluebell 1          | bb_1          | 7903  |
| Bluebell 2          | bb_2          | 9373  |
| Bluebell 3          | bb_3          | 7904  |
| Bluebell 4          | bb_4          | 7905  |
| Claycroft 1         | cc_1          | 7908  |
| Claycroft 2         | cc_2          | 7895  |
| Claycroft 3         | cc_3          | 9353  |
| Cryfield Village    | cryfield      | 9351  |
| Heronbank East      | hb_east       | 7899  |
| Heronbank West      | hb_west       | 9352  |
| International House | int_house     | 7902  |
| Jack Martin 3       | jm_3          | 7906  |
| Lakeside 1          | ls_1          | 7897  |
| Lakeside 4          | ls_4          | 7898  |
| Sherbourne 1        | sb_1          | 5982  |
| Sherbourne 5        | sb_5          | 5981  |
| Sherbourne 7        | sb_7          | 5983  |
| Tocil               | tocil         | 7907  |



