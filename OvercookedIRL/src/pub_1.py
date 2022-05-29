
import paho.mqtt.client as mqtt
import speech_recognition as sr
import threading
from threading import Thread
import pronouncing as pr
import time
import os

# http://www.steves-internet-guide.com/loop-python-mqtt-client/

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: "+str(rc))

    client.subscribe("overcooked_mic1", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Exepcted Disconnect')

r = sr.Recognizer()

# a global variable that holds the function that can be used to stop the microphone
global_stop_listening = None

# the default message callback
# wont be used if only publishing, but can still exist
def on_message(client, userdata, message):
    msg = str(message.payload)[2:][:-1]
    
    print('Received message: ' + msg + " on topic " + message.topic + '" with QoS ' + str(message.qos))
    #print(message.payload)
    # if(str(message.payload) == "b'" + "start" + "'"):
        # client.publish("tomato")
    #print('match')

    if(str(message.payload) == "b'" + "stop" + "'"):
        client.loop_stop()
        client.disconnect()
        return

    if(msg == "Start"):
        perform_speech()
    elif(msg == "Mic Stop"):
        # user wants to stop speech recognition in the middle of it
        global global_stop_listening
        if(global_stop_listening is not None):
            print('Stop listening- user cancel')
            global_stop_listening(wait_for_stop=False)

    stir = False
    chop = False

    if(msg == 'u'):
        client.publish('overcooked_game', "Pick Up", qos=1)
    elif(msg == 'd'):
        client.publish('overcooked_game', "Put Down", qos=1)
    elif(msg == 'cd'):
        client.publish('overcooked_game', "Chop", qos=1)
        # chop = True
    elif(msg == 'sd'):
        client.publish('overcooked_game', "Stir", qos=1)
        # stir = True
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
    # else:
    #     client.publish('overcooked_game', "Mic Stop", qos=1)

    chop_count = 0
    stir_count = 0

    if(chop):
        while(chop_count < 3):
            client.publish('overcooked_game', "Chop", qos=1)
            print('send chop')
            time.sleep(5)
            chop_count += 1
    if(stir):
        while(stir_count < 3):
            client.publish('overcooked_game', "Stir", qos=1)
            print('send stir')
            time.sleep(5)
            stir_count += 1

rhyme_dict = {}
first_phones = {}
commands = ['up', 'down', 'tomato', 'bread', 'lettuce', 'meat', 'plate', 'stone']
for cmd in commands: 
    rhyme_dict[cmd] = pr.rhymes(cmd)
    pronounce = pr.phones_for_word(cmd)[0].split()
    if len(pronounce) >= 2: # if the word takes 2(+) phones, consider first two phones
        first_phones[cmd] = pronounce[0]+pronounce[1]
    else: # if the word only is 1 phone, consider only the first phone
        first_phones[cmd] = pronounce[0]

print(first_phones)
# input('lol')

def perform_speech():
    m = sr.Microphone()    
    # with m as source:
    #     r.adjust_for_ambient_noise(source)

    # stop_listening is a function that is returned by listen_in_background
    # when called, it will stop the background listening process
    # listen_in_background spawns a background thread that repeatedly listens for phrases until stop_listening is called
    global global_stop_listening
    print("save stop listening in the next line")
    global_stop_listening = r.listen_in_background(source=m, callback=complete_speech_recognition,phrase_time_limit=1.5)
    print("/ Say something!")
    # save stop_listening into a global variable that can be called anywhere
    # global global_stop_listening
    # global_stop_listening = stop_listening

def complete_speech_recognition(recognizer, audio):
    print('stop listening- phrase found')
    global global_stop_listening
    global_stop_listening(wait_for_stop=False)
    global_stop_listening = None
    print('num threads')
    print(threading.active_count())
    game_msg = ""
    imu_msg = ""
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        line = recognizer.recognize_google(audio)
        #line.lower()
        print("Google Speech Recognition thinks you said " + line)
        speech_log.write(line + "/n")
        pronounce = pr.phones_for_word(line)[0].split()
        first2phones = ''
        if len(pronounce) >= 2:
            first2phones = pronounce[0]+pronounce[1]
        else:
            first2phones = pronounce[0]
        if(line == 'pickup' or line in rhyme_dict['up'] or first2phones == first_phones['up']):
            game_msg = "Pick Up"
            imu_msg = "Mic Stop"
        elif(line == 'down' or line in rhyme_dict['down'] or first2phones == first_phones['down'] or line == 'stone' or line in rhyme_dict['stone'] or first2phones == first_phones['stone']):
            game_msg = "Put Down"
            imu_msg = "Mic Stop"
        elif(line == 'tomato' or line in rhyme_dict['tomato'] or first2phones == first_phones['tomato']):
            game_msg = "Tomato"
            imu_msg = "Mic Stop"
        elif(line == 'bread' or line in rhyme_dict['bread'] or first2phones == first_phones['bread']):
            game_msg = "Bun"
            imu_msg = "Mic Stop"
        elif(line == 'lettuce' or line in rhyme_dict['lettuce'] or first2phones == first_phones['lettuce']):
            game_msg = "Lettuce"
            imu_msg = "Mic Stop"
        elif(line == 'meat' or line in rhyme_dict['meat'] or first2phones == first_phones['meat']):
            game_msg = "Meat"
            imu_msg = "Mic Stop"
        elif(line == 'plate' or line in rhyme_dict['plate'] or first2phones == first_phones['plate']):
            game_msg = "Plate"
            imu_msg = "Mic Stop"
        elif(line == 'trash'): # need to implement later
            game_msg = "Trash"
            imu_msg = "Mic Stop"
        else:
            game_msg = "Mic Stop"
            imu_msg = "Mic Stop"
    except sr.UnknownValueError:
        line = "count not understand audio"
        print("Google Speech Recognition could not understand audio")
        speech_log.write(line + "/n")
        game_msg = "Mic Stop"
        imu_msg = "Mic Stop"
    except sr.RequestError as e:
        line = "could not request results"
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        speech_log.write(line + "/n")
        game_msg = "Mic Stop"
        imu_msg = "Mic Stop"

    client.publish('overcooked_imu', imu_msg, qos=1)
    client.publish('overcooked_game', game_msg, qos=1)

    print('sent message')


i = 0
while os.path.exists("speech%s.txt" % i):
    i += 1
speech_log = open("speech" + str(i) + ".txt", "a")
    
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