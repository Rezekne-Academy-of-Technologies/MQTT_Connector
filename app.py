import requests
from flask import Flask
import json
import paho.mqtt.client as mqtt
import time
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def RoomData():

    dummy_rta_all_rooms = []  # |USED AS A PLACEHOLDER| Dummy array for storing all registered rooms within RTA
    dummy_rta_leacture_rooms = []  # |USED AS A PLACEHOLDER| Dummy array for storing all the rooms where leactures take place
    dummy_active_rooms_list = []  # |USED AS A PLACEHOLDER| An array for keeping separate active and not active rooms

    rta_active_output = []  # List w/ active rooms that ultimately get displayed
    rta_not_active_output = []  # List w/ NOT active rooms that also ultimately get displayed

    now = datetime.now()  # Setting up current-time
    current_time = now.strftime("%H:%M")

    rta_rooms_info_url = 'https://vis.rta.lv/service/busyrooms/rooms'
    active_rooms_url = 'https://vis.rta.lv/service/busyrooms/lectures'

    rta_rooms_response = requests.get(rta_rooms_info_url)  # W/ GET method we retrieve all the data from links
    rta_active_rooms_response = requests.get(active_rooms_url)

    if rta_rooms_response.status_code == 200 and rta_active_rooms_response.status_code == 200:
        print("Connection established! ")

        rooms_info = rta_rooms_response.content.decode()  # Returns the original string from encoded string
        active_rooms = rta_active_rooms_response.content.decode()

        response_rooms_info = json.loads(
            rooms_info)  # Used to parse a valid JSON string and convert it into a Python Dic
        response_active_rooms = json.loads(active_rooms)

        for room_active in response_active_rooms["Saraksts"]:
            if room_active['sakuma_laiks'] <= current_time and room_active['beigu_laiks'] >= current_time:
                rta_active_output.append({
                    "room_name": room_active['telpa'],
                    "date": room_active['datums_p'],
                    "status": "active"
                })
            else:
                rta_active_output.append({
                    "room_name": room_active['telpa'],
                    "date": room_active['datums_p'],
                    "status": "currently isn't active "
                })

        for room in response_rooms_info["Saraksts"]:  # All registered rooms within RTA are in RTA_ALL_ROOMS array
            dummy_rta_all_rooms.append(room['telpa'])

        for room_active in response_active_rooms[
            "Saraksts"]:  # All rooms where leactures are happening are in RTA_LEACTURES_ROOMS array
            dummy_rta_leacture_rooms.append(room_active['telpa'])

        for roomd_id in dummy_rta_all_rooms:
            if dummy_rta_leacture_rooms.__contains__(roomd_id):
                dummy_active_rooms_list.append(roomd_id + " active")
            else:
                rta_not_active_output.append({
                    "room_name": roomd_id,
                    "status": "not active today"
                })

        # return rta_active_output + rta_not_active_output

        # Connection to a MQTT broker

        def on_log(client, userdata, buf):  # Call back function
            print('log: ' + buf)

        def on_connect(client, userdata, flags, rc):  # Call back function
            if rc == 0:
                print('Connected successfully')
            else:
                print('Bad connection. Code: ' + str(rc))

        def on_disconnect(client, userdata, flags, rc=0):  # Call back function
            print('Disconnected result code ' + str(rc))

        broker = "192.168.69.2"
        client = mqtt.Client("python01")  # Creating a client that sends/publishes messages/data

        client.on_connect = on_connect  # Bind call back functions (line 61-63)
        client.on_disconnect = on_disconnect
        client.on_log = on_log

        print("Connecting to broker", broker)

        client.connect(broker)  # Establish connection
        client.loop_start()  # Start looping so that call back functions start to proccess
        data_out = json.dumps(rta_active_output + rta_not_active_output)  # to convert python dictionary or list (encoding object to JSON)
        client.publish("RTA/rooms", data_out)  # Publishing the data/messages
        time.sleep(4)
        client.loop_stop()  # End the loop
        client.disconnect()

    else:
        if rta_rooms_info_url != 200 and active_rooms_url != 200:
            print(" Error code for rta_rooms_response " + str(rta_rooms_response.status_code))
            print(" Error code for rta_active_rooms_response " + str(rta_active_rooms_response.status_code))
        else:
            if rta_rooms_info_url != 200:
                print(" Error code for rta_rooms_response°" + str(rta_rooms_response.status_code))
            else:
                print(" Error code for rta_active_rooms_response " + str(rta_active_rooms_response.status_code))

    return "Everything's been sent to MQTT: => 192.168.69.2"


if __name__ == "__main__":
    app.run()