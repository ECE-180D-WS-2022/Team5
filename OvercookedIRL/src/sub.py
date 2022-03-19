import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("connection returned result:" + str(rc))

    client.subscribe("overcooked_game", qos=1)


def on_disconnect(client, userdata, rc):
    if rc != 0: 
        print('Undexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    print('Received message: "' + str(message.payload) + " on topic " + message.topic + '" with QoS ' + str(message.qos)) 
    if(str(message.payload) == "b\'" + "tomato" + "\'"):
        # client.publish("tomato")
        # client.publish('overcooked_mic', 'tomato', qos=1)
        print("recieved tomato")

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async("test.mosquitto.org")
client.connect("test.mosquitto.org", 1883, 60)

# client.loop_start()
client.publish('overcooked_mic', "c", qos=1)
print('send')
client.loop_forever()
# while True: # perhaps add a stopping condition using some break or something.
#     pass # do your non-blocked other stuff here, like receive IMU data or something.
while(True):
    # client.loop_start()
    pass
# client.publish('overcooked_mic', "start", qos=1)

# client.loop_stop()
# client.disconnect()