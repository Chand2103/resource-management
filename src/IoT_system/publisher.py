import time
import paho.mqtt.client as paho
import ssl

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload.decode()))

client = paho.Client(client_id="chand2", protocol=paho.MQTTv5)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message

client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
client.username_pw_set("cam_sensor", "Cam_sensor1")

try:
    client.connect("94d44a09789645218d8b03ea9f6d2da0.s1.eu.hivemq.cloud", 8883)
except ssl.SSLError as e:
    print(f"SSL error: {e}")
    exit(1)

client.loop_start()  

while True:  
    client.publish("Lab L3/motion", payload="test", qos=1)
    time.sleep(2) 

