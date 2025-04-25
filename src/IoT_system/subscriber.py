import time
import paho.mqtt.client as paho
import ssl
import requests
import json
import pytz
from datetime import datetime
client = paho.Client(client_id="chand3", protocol=paho.MQTTv5)

client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
client.username_pw_set("cam_sensor", "Cam_sensor1")


sl_tz = pytz.timezone('Asia/Colombo')
last_msg_recived_at = datetime.now(sl_tz)

def time_to_minutes(time_str):
    
    t = datetime.strptime(time_str, "%H:%M:%S")
    return t.hour * 60 + t.minute

def fetch_and_check_bookings(sl_tz, last_msg_recived_at):
    curr_time = datetime.now(sl_tz)

    curr = time_to_minutes(curr_time)
    last = time_to_minutes(last_msg_recived_at)

    date = datetime.today().date()
    params = {
        "resource_name": "L3",
        "booked_date": date
    }

    response = requests.get("http://127.0.0.1:8000/get-bookings", params=params)
    if response.status_code == 200:
        response_data = response.json()
        start_times = response_data.get("startimes", [])
        end_times = response_data.get("endtimes", [])
        start_times = [time_to_minutes(t) for t in start_times]
        end_times = [time_to_minutes(t) for t in end_times]
        ids = response_data.get("ids",[])

        for i in range(0,len(start_times)):
            if (start_times[i]<=curr<=end_times[i]) and (start_times[i]<=last<=end_times[i]):
                url = "http://127.0.0.1:8000/delete-booking"
                data = {"booking_id": ids[i]}
                requests.delete(url, json=data)
                break
            else :
                print("no deletion is required")
    else:
        print("Request failed:", response.status_code, response.text)


def on_message(client, userdata, msg):
    global last_msg_recived_at,sl_tz
    if datetime.now(sl_tz) - last_msg_recived_at > 16: ## here 16 seconds is used only for testing purposes
        fetch_and_check_bookings(sl_tz, last_msg_recived_at)
        last_msg_recived_at = datetime.now(sl_tz)
    
    message = msg.payload.decode()
    if message == "Motion detected":
        last_msg_recived_at = datetime.now(sl_tz)

    print(message)

try:
    client.connect("94d44a09789645218d8b03ea9f6d2da0.s1.eu.hivemq.cloud", 8883)
except ssl.SSLError as e:
    print(f"SSL error: {e}")
    exit(1)

client.on_message = on_message

client.subscribe("Lab L3/motion")

client.loop_forever()