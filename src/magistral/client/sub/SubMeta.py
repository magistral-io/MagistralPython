'''
Created on 11 Aug 2016
@author: rizarse
'''

class SubMeta(object):
    
    def __init__(self, group, topic, channel, endPoints = None):
        self.__group = group
        self.__topic = topic        
        self.__endPoints = endPoints
        self.__channel = channel;
    
    def group(self):
        return self.__group;
    
    def topic(self):
        return self.__topic;
    
    def channel(self):
        return self.__channel;
    
    def endPoints(self):
        return self.__endPoints;