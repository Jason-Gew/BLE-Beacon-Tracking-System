# BLE Beacon Identification & Tracking System
# Ge Wu  July/7/2015
# Copyright (C) 2015-2016 Ge Wu <jason.ge.wu@gmail.com>
# This file is part of C2M Beacon Tracking System.
# C2M Beacon Tracking System can not be copied and/or distributed without the express
# Permission of Ge Wu

# Deprecated

import time
import datetime
import blescan
import sys
import os
import threading
import myTCP
import bluetooth._bluetooth as bluez

# Deprecated

new_apikey = ''
new_feedid = 'W57OsjCmhFSCxii6vLsq1A3Ar5ksbFzrst1A09lKTwg='
dev_id = 0
beacon = ''
reg_beacon = []
watch_dict = {}
dur_dict = {}
countdown = 11
entry_evnt = 'Entry'
exit_evnt = 'Exit'
error_evnt = 'Error'
list_room = []
lookup = ()

##################### Information #####################
print "\n+-----------------------------------------------+\n"
print "+    Welcome to use Beacon Tracking System !    +"
print "\n+----------------- Version 1.3 -----------------+\n"
#######################################################

##  Preset BLE dongle to up running  ##
cmd = os.popen('sudo hciconfig hci0 up').read()


## Pre-open registered beacons.txt file to check Beacon IDs ##
if (os.path.isfile('/home/linaro/BLE/registered beacons.txt')):
        create_time = os.path.getctime('/home/linaro/BLE/registered beacons.txt')
        with open('/home/linaro/BLE/registered beacons.txt','r') as f:
                for IDs in f.readlines():
                        IDs = IDs.strip('\n')
                        reg_beacon.append(IDs)
                f.close()
	print 'Beacon ID file Created at: ',time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())),'\n'
	
else:
        print 'Cannot find Registered Beacon ID file!'

try:

	sock = bluez.hci_open_dev(dev_id)
	print '\nBeacon Tracking Initiating...'
	##Full MSG Format: MAC/uuid/Major/Minor/TX-Power/RSSI'

except:
	print 'Error: Cannot Initialize Bluetooth Device...'
        print 'Error: ',cmd
	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

edge_id = raw_input('Please Enter Edge Device ID: ')
rssi_threshold = int(raw_input('Please Enter Correct RSSI Threshold: '))
if rssi_threshold>90 or rssi_threshold<20:
    print 'Please Enter Valid RSSI Threshold! (20;90)'
    sys.exit(1)
else:
    pass

if new_apikey!= '':
        myTCP.apikey = new_apikey

if new_feedid!= '': 
        myTCP.feedId = new_feedid

##---------------------------------------------------------------------##

##def data_rssi(person_num, rssi_value):
##        
##        ###
                
        
        
def update(beaconID,Event_ID,Event_time,Duration):

        message = 'beaconID,'+beaconID+'|edgeID,'+edge_id+'|time,'+str(Event_time)[0:19]
        message = message+'|EventID,'+str(Event_ID)+'|duration,'+str(Duration)
        check = myTCP.TCP_Send(message)
        if check:        
            del message
        else:
            check = myTCP.TCP_Send(message)
            
                
def event_ctrl(site,rssi):
        duration = 0
        sys_lock.acquire()
        if reg_beacon[site] not in list_room:
                entry_time = datetime.datetime.now()
                list_room.append(reg_beacon[site])
                dur_dict[reg_beacon[site]] = entry_time
                update(reg_beacon[site],entry_evnt,entry_time,duration)
        watch_dict[reg_beacon[site]] = countdown
##        print '\nBeacons in Room-'+str(edge_id)+': ',list_room,'\n'
        sys_lock.release()       


def ble_track(rssi_threshold):
        uid = beacon[18:50]       ## Full uid range is [18:50]
        length = len(beacon)
        rssi = beacon[length-2:length]
        if int(rssi)<rssi_threshold and int(rssi)>20:   ## RSSI Threshold check
                if uid in reg_beacon:
                        position = reg_beacon.index(uid)                        
                        event_ctrl(position,rssi)
                else:
                        pass                
        else:
                print 'Continue tracking...'
                
class system_main(threading.Thread):

        def __init__(self):
		threading.Thread.__init__(self)

                
	def run(self):
                while True:                 
                        global list_room, beacon, watch_dict
                        returnedList = blescan.parse_events(sock, 5)
                        print "------------------------------------------------"
                        for beacon in returnedList:
##		                    print beacon
                            ble_track(rssi_threshold)
##                          list_room = list(set(list_room))

                        
                                
class watchdog(threading.Thread):
        
        def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
                global list_room, watch_dict
                while True:
                        time.sleep(1)
                        if watch_dict:
                                temp_list = []
                                for key in watch_dict or dur_dict:
                                        watch_dict[key] -= 1
                                        print watch_dict
                                        if watch_dict[key] <= 0:
                                                temp_list.append(key)
                                                exit_time = datetime.datetime.now()
                                                sys_lock.acquire()
                                                list_room.remove(key)
                                                duration = (exit_time-dur_dict[key]).seconds
                                                update(key,exit_evnt,exit_time,duration)
                                                sys_lock.release()
                                                print 'Beacon: '+ key +' Exit! Duration: '+str(duration)+' Seconds!\n'
                                if temp_list:
                                        sys_lock.acquire()
                                        for key in temp_list:
                                                del watch_dict[key]
                                                del dur_dict[key]
                                        sys_lock.release()



thread1 = system_main() 
thread2 = watchdog()

sys_lock = threading.Lock()

thread1.start()
thread2.start()


		

