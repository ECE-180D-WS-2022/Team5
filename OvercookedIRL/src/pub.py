import paho.mqtt.client as mqtt
import speech_recognition as sr
import time
import os

# http://www.steves-internet-guide.com/loop-python-mqtt-client/

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: "+str(rc))

    client.subscribe("overcooked_mic", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Exepcted Disconnect')

# the default message callback
# wont be used if only publishing, but can still exist
def on_message(client, userdata, message):
    msg = str(message.payload)[2:][:-1]
    print('Received message: ' + msg + " on topic " + message.topic + '" with QoS ' + str(message.qos))
    print(message.payload)
    # if(str(message.payload) == "b'" + "start" + "'"):
        # client.publish("tomato")
    print('match')

    if(str(message.payload) == "b'" + "stop" + "'"):
        client.loop_stop()
        client.disconnect()
        return

    # client.publish('overcooked_game', 'tomato', qos=1)
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            line = r.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + line)
            speech_log.write(line + "/n")
            # client.publish('overcooked_game', line, qos=1)
        except sr.UnknownValueError:
            line = "count not understand audio"
            print("Google Speech Recognition could not understand audio")
            # client.publish('overcooked_game', line, qos=1)
            speech_log.write(line + "/n")
        except sr.RequestError as e:
            line = "could not request results"
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            # client.publish('overcooked_game', line, qos=1)
            speech_log.write(line + "/n")
    # time.sleep(5)
    chop = False
    chop_count = 0
    stir = False
    stir_count = 0

    if (not chop and not stir):
        if(msg == 'u'):
            client.publish('overcooked_game', "Pick Up", qos=1)
        elif(msg == 'd'):
            client.publish('overcooked_game', "Put Down", qos=1)
        elif(msg == 'cd'):
            # client.publish('overcooked_game', "Chop", qos=1)
            chop = True
        elif(msg == 'sd'):
            # client.publish('overcooked_game', "Stir", qos=1)
            stir = True
        elif(msg == 't'):
            client.publish('overcooked_game', "Tomato", qos=1)
        elif(msg == 'b'):
            client.publish('overcooked_game', "Bun", qos=1)
        elif(msg == 'l'):
            client.publish('overcooked_game', "Lettuce", qos=1)
        elif(msg == 'm'):
            client.publish('overcooked_game', "Meat", qos=1)
        elif(msg == 'p'):
            client.publish('overcooked_game', "Plate", qos=1)
        else:
            client.publish('overcooked_game', "other", qos=1)
    if(chop):
        while(chop_count < 3):
            client.publish('overcooked_game', "Chop", qos=1)
            print('send chop')
            time.sleep(5)
            chop_count += 1

        chop_count = 0
        chop = False
    if(stir):
        while(stir_count < 3):
            client.publish('overcooked_game', "Stir", qos=1)
            print('send stir')
            time.sleep(5)
            stir_count += 1

        stir_count = 0
        stir = False
    

    print('sent message')


i = 0
while os.path.exists("speech%s.txt" % i):
    i += 1
speech_log = open("speech" + str(i) + ".txt", "a")
# self.r = sr.Recognizer()
    
r = sr.Recognizer()
# 1. create a client instance
client = mqtt.Client()

# add additional client options (security, certifications, etc.)
# many default options should be good to start off
# add callbacks to client

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# connect to a broker using one of the connect functions
client.connect_async("test.mosquitto.org")
client.connect("test.mosquitto.org", 1883, 60)
# client.connect("localhost", 1883, 60)

# call one of the loop*() functions to maintain network traffic flow wit the broker
# client.loop_start()

# use subscribe() to subscrive to a topic and receive messages

# 5. use publish() to publish messages to the broker.
# payload must be a string, bytearray, int, float or None.
client.loop_forever()
# print('Publishing...')
# for i in range(10):
#     print(i)
#     client.publish('team5', 'hi', qos=1)

# use disconnect() to disconnect from the broker
client.loop_stop()
client.disconnect()