'''
Created on 9 Aug 2016

@author: rizarse
'''
import paho.mqtt.client.Client as mqtt
# from paho.mqtt.client import Client


class MqttClient(mqtt):
    

    def __init__(self, params):
        '''
        Constructor
        '''
        