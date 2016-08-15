'''
Created on 13 Aug 2016

@author: rizarse
'''
import time

class PubMeta(object):
    
    __topic = None
    __timestamp = 0;
    __channel = -1;

    def __init__(self, topic, channel, timestamp = int(round(time.time() * 1000))):
        self.__topic = topic;
        self.__channel = channel;
        self.__timestamp = timestamp;
        
    def topic(self):
        return self.__topic;
    
    def channel(self):
        return self.__channel;
        
    def timestamp(self):
        return self.__timestamp;