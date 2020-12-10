import paho.mqtt.client as mqtt
import json

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("received...")
    print(msg.topic+" "+str(msg.payload))

def on_log(client,userData,level,buf):
    print("log: ",buf)

client = mqtt.Client("incubator101xxx")
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log

client.connect("mqtt.eclipse.org", 1883, 60)

client.subscribe("incubator101/machine")
client.publish("incubator101/machine","yess")

print("connected na.")


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

