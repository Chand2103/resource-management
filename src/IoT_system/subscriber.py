import time
import paho.mqtt.client as paho
import ssl
import requests
import json
client = paho.Client(client_id="chand3", protocol=paho.MQTTv5)

client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
client.username_pw_set("cam_sensor", "Cam_sensor1")

last_msg_recived_at = time.time()

def on_message(client, userdata, msg):
    global last_msg_recived_at
    if time.time() - last_msg_recived_at > 1800:
        data = {
            "sensor_id": "cam1",
            "status": "motion_detected",
            "timestamp": time.time()
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post("http://127.0.0.1:8000/get-bookings", headers=headers, data=json.dumps(data))
        print(response)
    
    message = msg.payload.decode()
    if message == "Motion detected":
        last_msg_recived_at = time.time()

    print(message)

try:
    client.connect("94d44a09789645218d8b03ea9f6d2da0.s1.eu.hivemq.cloud", 8883)
except ssl.SSLError as e:
    print(f"SSL error: {e}")
    exit(1)

client.on_message = on_message

client.subscribe("Lab L3/motion")

client.loop_forever()