from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/washer', methods=['GET'])
def washer():
    room = request.args.get('room')
    machine_number = request.args.get('machine_number')

    if not room:
        return jsonify({"error": "Room parameter is required"}), 400

    if machine_number:
        try:
            machine_number = int(machine_number)
        except ValueError:
            return jsonify({"error": "Machine number must be an integer if provided"}), 400

    room_data = {"ww_arden": 7894, "ww_bericote": 9269, "ww_compton": 9271, "ww_dunsmere": 9267, "ww_emscote": 9268, "ww_feldon": 7896, "ww_gosford": 9270, "ww_hampton": 9276, "ww_kinghtcote": 9275, "ww_loxley": 9273, "av_1": 9274, "av_2": 9272, "av_3": 9354, "bf_1": 7900, "bf_2": 7901, "bb_1": 7903, "bb_2": 9373, "bb_3": 7904, "bb_4": 7905, "cc_1": 7908, "cc_2": 7895, "cc_3": 9353, "cryfield": 9351, "hb_east": 7899, "hb_west": 9352, "int_house": 7902, "jm_3": 7906, "ls_1": 7897, "ls_4": 7898, "sb_1": 5982, "sb_5": 5981, "sb_7": 5983, "tocil": 7907}

    if room not in room_data:
        return jsonify({"error": "Invalid room name"}), 400

    response = requests.get(f'https://api.alliancelslabs.com/washAlert/machines/{room_data[room]}', headers={'alliancels-organization-id': '652210'})

    data = response.json()

    attributes_to_remove = ["id", "serialNumber", "modelNumber", "networkController", "networkNode", "controlId", "machineGeneration", "organization", "room", "machineAuditType", "installedDate", "lastCollectionDate", "lastProcessedDate", "createdAt", "createdBy", "updatedAt", "updatedBy", "washAlertXAxis", "washAlertYAxis", "washAlertScaleX", "washAlertScaleY", "machineName", "machineAuditGroupType", "washAlertAngle", "washAlertIsVisible", "machineNote", "coinVaultSize", "lastKnownProgram", "lastKnownProgramUpdatedAt", "washAlertZIndex", "machineTypeRecord", "guid", "isExternal"]

    current_status_attributes_to_remove = ['canTopOff', 'controlId', 'createdAt', 'displayStatus', 'gatewayName', 'id', 'linkQualityIndicator', 'receivedAt', 'roomId', 'selectedModifier', 'topOffTime', 'topOffVend', 'uuid']

    modified_data = {}

    for obj in data:
        for attribute in attributes_to_remove:
            if attribute in obj:
                del obj[attribute]

        if "machineNumber" in obj:
            machineNumber = obj["machineNumber"]
            obj["machineNumber"] = int(machineNumber)

        if "machineType" in obj and "id" in obj["machineType"]:
            del obj["machineType"]["id"]

        if "currentStatus" in obj:
            obj["currentStatus"] = json.loads(obj["currentStatus"])

            for attribute in current_status_attributes_to_remove:
                if attribute in obj["currentStatus"]:
                    del obj["currentStatus"][attribute]

        modified_data[int(machineNumber)] = obj

    modified_json_data = json.dumps(modified_data)

    if machine_number:
        if machine_number in modified_data:
            return jsonify(modified_data[machine_number])
        else:
            return jsonify({"error": "Machine number not found in the data"}), 404
    else:
        return jsonify(modified_data)

@app.errorhandler(404)
def page_not_found(e):
    return "Invalid route", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
