'''
Created on 11 Aug 2016
@author: rizarse
'''

import time
import logging
from threading import Thread
from kafka.consumer.group import KafkaConsumer
from magistral.client.Configs import Configs
from magistral.client.MagistralException import MagistralException
from kafka.structs import TopicPartition
from magistral.Message import Message

class GroupConsumer(Thread):
        
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO) 
    
    def __init__(self, sKey, bootstrapServers, groupId, permissions, cipher = None):
        
        super(GroupConsumer, self).__init__();
        
        self.group = groupId;
        self.subKey = sKey;
        
        self.cipher = None if cipher is None else cipher;
                
        configs = Configs.consumerConfigs();
        configs["bootstrap_servers"] = bootstrapServers;
        configs["group_id"] = groupId;
        configs['enable_auto_commit'] = False;
        
        self.__isAlive = True;
        
        self.__configs = {}
        self.__configs.update(configs);
        
        self.__consumer = KafkaConsumer(bootstrap_servers = bootstrapServers, enable_auto_commit = False, group_id = groupId);
        
        self.permissions = permissions;
        self.map = {}
        
        self.__offsets = {}

    def run(self):
        
        while self.__isAlive:
            try:
#               SET POINTERS
                
                shifts = False;
                    
                for x in self.__consumer.assignment():
                    
                    if x not in self.__offsets:
                        cur = self.__consumer.committed(x);
                        
                        if cur is None: 
                            self.__consumer.seek_to_beginning();
                            earliest = self.__consumer.position(x);
                            self.__offsets[x] = earliest;
                        else:
                            self.__offsets[x] = cur;
                                        
                    self.__consumer.seek_to_end();        
                    last = self.__consumer.position(x);
                    
                    offset = self.__offsets[x];
                    
                    if last - 1 <= offset: continue                    
                    shifts = True;
                        
                    self.__consumer.seek(x, offset + 1);
                    
#               FETCH DATA
                
                if shifts == False:
                    time.sleep(0.5);
                    continue;
                
                def recordsTotally(data):
                    size = 0;
                    for val in data.values(): 
                        if len(val) > 0: size = size + len(val);                        
                    return size;
                
                data = self.__consumer.poll(1024);
                
                def consumerRecord2Message(record):                    
                    payload = record[6]
                                        
                    if self.cipher is not None:
                        try:
                            payload = self.cipher.decrypt(payload)
                        except:
                            pass
                                        
                    msg = Message(record[0], record[1], payload, record[2], record[3])
                    return msg
                
                while recordsTotally(data) > 0:
                    
                    for x, values in data.items():
                        
                        highest = self.__offsets[x];
                    
                        for value in values:
                            msg = consumerRecord2Message(value);
                                                        
                            if x in self.__offsets and msg.index() > highest:
                                listener = self.map[msg.topic()][msg.channel()];
                                
                                listener(msg);
                                highest = msg.index();
                            
                        self.__offsets[x] = highest;                            
                    
                    self.__consumer.commit_async({x, self.__offsets[x]});
                    
                    self.__consumer.seek(x, self.__offsets[x]);
                    data = self.__consumer.poll(200);        
                    
            except:
                pass

    
#   ////////////////////////////////////////////////////////////////////////////////////    

    def subscribe(self, topic, channel = -1, listener = None, callback = None):
        
        assert channel is not None and isinstance(channel, int), "Channel expected as int argument"        
        if (channel < -1): channel = -1;
                
        etopic = self.subKey + "." + topic;
        
        if (etopic not in self.__consumer.topics()):
            self.logger.error("Topic [" + topic + "] does not exist");
            raise MagistralException("Topic [" + topic + "] does not exist");
                    
        self.logger.debug("Subscribe -> %s : %s | key = %s", topic, channel, self.subKey);
        
        if (self.permissions == None or len(self.permissions) == 0): 
            raise MagistralException("User has no permissions for topic [" + topic + "].");
        
        self.fch = [];
        
        for meta in self.permissions:             
            if (meta.topic() != topic): continue;  
            
            if channel == -1:
                self.fch = meta.channels();
            elif channel in meta.channels():                          
                self.fch = [ channel ];  
        
        if (len(self.fch) == 0): 
            npgex = "No permissions for topic [" + topic + "] granted";
            self.logger.error(npgex);                                
            raise MagistralException(npgex);
        
        if (self.map == None or etopic not in self.map): 
            self.map[etopic] = {}
        
#         // Assign Topic-partition pairs to listen
        
        tpas = [];
        for ch in self.fch:            
            tpas.append(TopicPartition(etopic, ch));
            if (listener is not None): self.map[etopic][ch] = listener;        
        
        self.__consumer.assign(tpas);
        
        for key, val in self.__configs.items():
            self.__consumer.config[key] = val;
                
        if callback is not None : callback(self.__consumer.assignment());
        return self.__consumer.assignment();
        
        
    def unsubscribe(self, topic): 
        self.consumer.unsubscribe();
        self.map.remove(topic);
        
        tpas = [];
        for t, chm in self.map.items():
            for p in chm.keys(): tpas.append(TopicPartition(t, p))

        self.consumer.assign(tpas);
    