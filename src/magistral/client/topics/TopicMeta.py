'''
Created on 12 Aug 2016

@author: rizarse
'''

class TopicMeta(object):

    def __init__(self, topic, channels):
        self.__topicName = topic
        self.__channels = channels

    def topic(self):
        return self.__topicName
    
    def channels(self):
        return self.__channels