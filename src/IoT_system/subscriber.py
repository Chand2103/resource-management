import time
import paho.mqtt.client as paho
import ssl
client = paho.Client(client_id="chand3", protocol=paho.MQTTv5)

client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
client.username_pw_set("cam_sensor", "Cam_sensor1")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(message)

try:
    client.connect("94d44a09789645218d8b03ea9f6d2da0.s1.eu.hivemq.cloud", 8883)
except ssl.SSLError as e:
    print(f"SSL error: {e}")
    exit(1)

client.on_message = on_message

client.subscribe("Lab L3/motion")

client.loop_forever()