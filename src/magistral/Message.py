'''
Created on 13 Aug 2016
@author: rizarse
'''

class Message(object):

    __topic = None;
    __channel = -1;
    __body = None;
    __index = None;
    __timestamp = 0;

    def __init__(self, topic, channel, payload, index, timestamp):
        self.__topic = topic;
        self.__channel = channel;
        self.__body = payload;
        self.__index = index;
        self.__timestamp = timestamp;
    
    def topic(self):
        return self.__topic;
    
    def channel(self):
        return self.__channel;
    
    def payload(self):
        return self.__body;
    
    def index(self):
        return self.__index;
    
    def timestamp(self):
        return self.__timestamp;