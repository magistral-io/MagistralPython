'''
Created on 11 Aug 2016
@author: rizarse
'''

class SubMeta(object):
        
    __group = None;
    __topic = None;
    __endPoints = [];
    __channel = None;
    
    def __init__(self, group, topic, channel, endPoints = None):
        self.__group = group;
        self.__topic = topic;
        if (endPoints != None): self.__endPoints.append(endPoints);
        self.__channel = channel;
        pass;
    
    def group(self):
        return self.__group;
    
    def topic(self):
        return self.__topic;
    
    def channel(self):
        return self.__channel;
    
    def endPoints(self):
        return self.__endPoints;