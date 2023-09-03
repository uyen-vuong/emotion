#!/usr/bin/env python3
import paho.mqtt.client as mqtt
from django.conf import settings
import time 
import uuid
import json


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
class MQTT_Connection:
   
    _instance = None
    @staticmethod
    def getInstance():
        if MQTT_Connection._instance is None:
            MQTT_Connection._instance = MQTT_Connection()
        return MQTT_Connection._instance
    
    def __init__(self) -> None:

        # This is the Publisher
        self.client = mqtt.Client()

        self.client.connect(getattr(settings, "MQTT_HOST"),getattr(settings, "MQTT_PORT"), 60)
        self.client.username_pw_set(getattr(settings, "MQTT_USR"), getattr(settings, "MQTT_PASS"))

        print(getattr(settings, "MQTT_HOST"),getattr(settings, "MQTT_PORT"))
        print(getattr(settings, "MQTT_USR"), getattr(settings, "MQTT_PASS"))

        self.client.on_connect = on_connect
        self.client.loop_start()
        t = time.time()
        while True:
            print(self.client.is_connected())
            time.sleep(1)
            if self.client.is_connected():
                break 
            if time.time() - t > 10:
                break 
    
    def send(self, msg, topic):
        if self.client.is_connected():
            self.client.publish(topic, json.dumps(msg))
            print("Send to client")