# file: asynchronous-inquiry.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: demonstration of how to do asynchronous device discovery by subclassing
#       the DeviceDiscoverer class
# $Id: asynchronous-inquiry.py 405 2006-05-06 00:39:50Z albert $
#
# XXX Linux only (5/5/2006)

import bluetooth
import select
import sys

RSSI_THRESHOLD = -45

class MyDiscoverer(bluetooth.DeviceDiscoverer):
    
    def pre_inquiry(self):
        self.done = False
    
    def device_discovered(self, address, device_class, rssi, name):
        global mode 
	global mac
	global gname
     	if rssi >  RSSI_THRESHOLD:
 	   mac = address
	   gname = name
	   mode = "OK" 
         
    def inquiry_complete(self):
        self.done = True


def scan():

     global mac
     global gname
     global mode
     mac =""
     gname =""
     mode =""

     while True:
        d = MyDiscoverer()
        d.find_devices(duration=1, lookup_names = True)
	d.process_event()	
 	if  mode == "OK":
	  mode = "none"
	  break

