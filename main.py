import requests
import json

# All the other parameters in the header are not needed
headers = {
    'alliancels-organization-id': '652210'
}

# Dictionary containing wash room name and values
room_data = {"ww_arden": 7894, "ww_bericote": 9269, "ww_compton": 9271, "ww_dunsmere": 9267, "ww_emscote": 9268, "ww_feldon": 7896, "ww_gosford": 9270, "ww_hampton": 9276, "ww_kinghtcote": 9275, "ww_loxley": 9273, "av_1": 9274, "av_2": 9272, "av_3": 9354, "bf_1": 7900, "bf_2": 7901, "bb_1": 7903, "bb_2": 9373, "bb_3": 7904, "bb_4": 7905, "cc_1": 7908, "cc_2": 7895, "cc_3": 9353, "cryfield": 9351, "hb_east": 7899, "hb_west": 9352, "int_house": 7902, "jm_3": 7906, "ls_1": 7897, "ls_4": 7898, "sb_1": 5982, "sb_5": 5981, "sb_7": 5983, "tocil": 7907}

response = requests.get(f'https://api.alliancelslabs.com/washAlert/machines/{room_data["tocil"]}', headers=headers)

data = response.json()
json_string = json.dumps(data, indent=4)
print(json_string)