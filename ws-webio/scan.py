# file: asynchronous-inquiry.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: demonstration of how to do asynchronous device discovery by subclassing
#       the DeviceDiscoverer class
# $Id: asynchronous-inquiry.py 405 2006-05-06 00:39:50Z albert $
#
# XXX Linux only (5/5/2006)

import bluetooth
import select
import datetime
import time
import RPi.GPIO as GPIO
import multiprocessing


#Initialize Raspberry PI GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.OUT)
#global variable
RSSI_THRESHOLD = -50

def read():
  with open("user", "r") as ins:
    global array 
    array = []
    global id 
    id = 0
    for line in ins:
	array.append(line.rstrip('\n'))
	print array[id]
     	id += 1
def write_log(n,m):
    log = open("log","a")
    txt = "At: %s -->Name [%s] MAC [%s]  \n" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),n,m)
    log.write(txt)
    log.close()


class MyDiscoverer(bluetooth.DeviceDiscoverer):
    
    def pre_inquiry(self):
        self.done = False
    
    def device_discovered(self, address, device_class, rssi, name):
	print "[scan] find device ... "
	print rssi
#        GPIO.output(36,False)

        if any(address in s for s in array):
	   if rssi > RSSI_THRESHOLD:  	
	      print("[scan] Open for : Name [%s] MAC [%s] On: %s" % (name,address,datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))		
#	      write_log(name,address)
	      GPIO.output(36,True)	      
	      time.sleep(4)
  	      GPIO.output(36,False)
 	     
#        if rssi > RSSI_THRESHOLD:  	
#      	   print "[scan] found device !"
#           if any(address in s for s in array):
#              print("[scan] Open for : Name [%s] MAC [%s] On: %s" % (name,address,datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))		
#	      write_log(name,address)
#	      GPIO.output(36,True)	      
#    	      time.sleep(5)
#    	      GPIO.output(36,False)
	      	      	      	
    def inquiry_complete(self):
        self.done = True




GPIO.output(36,False)



def scan():  
  read()

  while True:    
     d = MyDiscoverer()
     d.find_devices(duration=1, lookup_names = True, flush_cache=True)
     d.process_event()
     

#    a = MyDiscoverer()
#    a.find_devices(duration=1, lookup_names = True)
#    a.process_event()

#    b = MyDiscoverer()
#    b.find_devices(duration=1, lookup_names = True)
#    b.process_event()

#    c = MyDiscoverer()
#    c.find_devices(duration=1, lookup_names = True)
#    c.process_event()

 #   e = MyDiscoverer()
 #   e.find_devices(duration=1, lookup_names = True)
 #   e.process_event()

 #   print "sa"

#    readfiles = [ d, ]
#    rfds = select.select( readfiles, [], [] )[0]
#    if d in rfds:
#       d.process_event()
#    print "asda"  
#    time.sleep(1)


#scan() 
#

