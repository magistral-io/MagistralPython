'''
Created on 9 Aug 2016

@author: rizarse
'''

import logging

class Configs:
    logging.basicConfig(level=logging.INFO,
                        format=('%(filename)s: '    
                                '%(levelname)s: '
                                '%(funcName)s(): '
                                '%(lineno)d:\t'
                                '%(message)s')
                        )
        
    @staticmethod
    def producerConfigs():
        producer = {}
        producer["producer_type"] = "async";
        producer["acks"] = "1"
        producer["retries"] = 5
        producer["batch_size"] = 32768
        producer["linger_ms"] = 5
        producer["request_timeout_ms"] = 60000        
        producer["buffer_memory"] = 33554432
        producer["key_serializer"] = None
        producer["value_serializer"] = None
        producer["compression_type"] = "gzip"
        return producer;
     
    @staticmethod   
    def consumerConfigs():
        consumer = {}
        consumer["enable_auto_commit"] = False;        
        consumer["session_timeout_ms"] = 30000       
        consumer["fetch_min_bytes"] = 64
        consumer["fetch_wait_max_ms"] = 128        
        consumer["max_partition_fetch_bytes"] = 262144
        
        consumer["buffer_memory"] = 33554432
        consumer["key_serializer"] = None
        consumer["value_serializer"] = None
        return consumer;
    
    