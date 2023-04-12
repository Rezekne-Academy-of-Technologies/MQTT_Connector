import requests
from flask import Flask
import json
import paho.mqtt.client as mqtt
import time
from datetime import datetime
from flask import render_template

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def RoomData():

    dummy_rta_all_rooms = []  # |USED AS A PLACEHOLDER| Dummy array for storing all registered rooms within RTA
    dummy_rta_lecture_rooms = []  # |USED AS A PLACEHOLDER| Dummy array for storing all the rooms where leactures take place
    dummy_active_rooms_list = []  # |USED AS A PLACEHOLDER| An array for keeping both active and not active rooms data

    rta_active_output = []  # List w/ active rooms that ultimately gets displayed
    rta_not_active_output = []  # List w/ NOT active rooms that also at the end gets displayed

    now = datetime.now()  # Setting up current-time
    current_time = now.strftime("%H:%M")

    rta_rooms_info_url = 'https://vis.rta.lv/service/busyrooms/rooms'
    active_rooms_url = 'https://vis.rta.lv/service/busyrooms/lectures'

    rta_rooms_response = requests.get(rta_rooms_info_url)  # With GET method we retrieve all the data from links
    rta_active_rooms_response = requests.get(active_rooms_url)

    if rta_rooms_response.status_code == 200 and rta_active_rooms_response.status_code == 200:
        print("Connection established! ")

        rooms_info = rta_rooms_response.content.decode()  # Returns the original string from encoded string
        active_rooms = rta_active_rooms_response.content.decode()

        response_rooms_info = json.loads(rooms_info)  # Used to parse valid JSON string and convert it into a Python Dictionary
        response_active_rooms = json.loads(active_rooms)

        for room_active in response_active_rooms["Saraksts"]:
            if (room_active['telpa'] == '1'):
                del room_active
            else:
                buildings = room_active['telpa'].split('-')
                if room_active['sakuma_laiks'] <= current_time and room_active['beigu_laiks'] >= current_time:
                    rta_active_output.append({
                        "room_name": room_active['telpa'],
                        "date": room_active['datums_p'],
                        "status": "active",
                        "building": buildings[1]

                    })
                else:
                    rta_active_output.append({
                        "room_name": room_active['telpa'],
                        "date": room_active['datums_p'],
                        "status": "currently isn't active ",
                        "building": buildings[1]

                    })

        for room in response_rooms_info["Saraksts"]:
            if (room['telpa'].__contains__('test') or room['telpa'] == '1' or room['telpa'] == 'Prakse - I'):
                del room['telpa']
            else:
                dummy_rta_all_rooms.append(room['telpa'])

        for room_active in response_active_rooms["Saraksts"]:
            dummy_rta_lecture_rooms.append(room_active['telpa'])

        for room_id in dummy_rta_all_rooms:
            building = room_id.split('-')
            if dummy_rta_lecture_rooms.__contains__(room_id):
                dummy_active_rooms_list.append(room_id + " active")
            else:
                rta_not_active_output.append({
                    "room_name": room_id,
                    "status": "not active today",
                    "building": building[1]

                })

        #return rta_active_output + rta_not_active_output
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

        client.connect(broker)  # Establishing connection
        client.loop_start()  # Beginning of the looping so that call back functions start to proccess
        data_out = json.dumps(rta_active_output + rta_not_active_output)  # Encoding object to JSON format
        client.publish("RTA/rooms", data_out)  # Publishing data/messages
        time.sleep(4)
        client.loop_stop()  # End of the loop
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

    return render_template('page.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=8887)