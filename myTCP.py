# TCP Client: Send Message to C2M Server /Python 2.7
# Program is written by Ge Wu
# Copyright (C) 2015-2016 Ge Wu <jason.ge.wu@gmail.com>
# This file is part of C2M Beacon Tracking System.
# C2M Beacon Tracking System can not be copied and/or distributed without the express
# Permission of Ge Wu

import socket
import time

TCP_IP = '199.108.99.62' # C2M TCP Server
TCP_PORT = 3001         # C2M TCP Port
BUFFER_SIZE = 1024
apikey = 'z7s1iZ1014kWrrVfukW1RolO39cEwg'
feedId = 'lkP8D7daIItGAIElTqr7l1TO9WvokENWoIGwrRgbDB8='

def TCP_Send(dat_MESSAGE):
    pre_MESSAGE = 'apikey:'+apikey+',feedId:'+feedId+',feed='

    MESSAGE = pre_MESSAGE + dat_MESSAGE
    length = len(MESSAGE)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    if s.send(MESSAGE):
        print 'TCP Message: ', MESSAGE
        print 'Sent time: ',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print 'Length of the Message is [ %d ]' % length
        return True
    else:
        print 'Try Again!'
        return False
    s.close()

def TCP_Receive():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    data = s.recv(BUFFER_SIZE)
    length = len(data)
    if cmp(data,'')!=0:
        print 'Received Data:', data
        print 'Received time: ',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print 'Length of the Message is [ %d ]' % length
    else:
        pass
    s.close()


