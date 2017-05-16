#! /usr/bin/python

import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import os
import signal
import subprocess
import RPi.GPIO as GPIO
import string
import random

from Naked.toolshed.shell import execute_js
import adduser2 as User
import threading
import multiprocessing
#Initialize Raspberry PI GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

#Tornado Folder Paths
settings = dict(
	template_path = os.path.join(os.path.dirname(__file__), "templates2"),
	static_path = os.path.join(os.path.dirname(__file__), "static2")
	)

#Tonado server port
PORT = 80

#Thread
#generate key
KEY_LEN = 4

class MainHandler(tornado.web.RequestHandler):
  def get(self):
     print "[HTTP](MainHandler) User Connected."
     self.render("index.html")

	
class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    print '[WS] Connection was opened.'
    self.update_user()

  def base_str(self):
    return (string.letters+string.digits)   
  def key_gen(self):
    keylist = [random.choice(self.base_str()) for i in range(KEY_LEN)]
    return ("".join(keylist))
     
  def write_user(self,str1):
    print "[user.txt] \nUser now------------------------------"
    User.read()
    print "---------------------------------------------------"
    if any(str1 in s for s in User.array):
	print "[sys] This User is already User "
    else :
	password = self.key_gen()
	print password
	us = open("user2","a")
    	id = User.id + 1 
    	txt = "ID/%s/Password/%s/Username/%s \n" %(str(id),password,str1)
    	us.write(txt)
    	us.close()
  def update_user(self):
        with open("user2", "r") as ins:
    	  array = []
    	  id = 0
          ud = "update"
    	  for line in ins:
             array.append(line.rstrip('\n'))
	     ud += "," + array[id]
             id += 1
 	  self.write_message(ud)
  def remove_user(self,index,name):
	with open("user2", "r") as ins:
          array = []
          for line in ins:
             array.append(line.rstrip('\n'))
     
        del array[int(index)]
        open("user2", 'w').close()
	us = open("user2","a")
        count = 0
	id = 1
	for add in array:
          if count != index:
            txt = "ID [%s] %s\n" %(str(id),array[count][7:])
            us.write(txt)
          count += 1
	  id += 1
        us.close()
	self.update_user()

  def on_message(self, message):
    print '[WS] Incoming message:', message
    if message == "on_g":
      GPIO.output(16, True)
    if message == "off_g":
      GPIO.output(16, False)
    if "adduser" in message:
      print "[sys] Adding user..."
      data = message.split(",")
      self.write_user(str(data[1]))  
      print "[sys] Addition complete"
      self.update_user()	
    if message == "start":
      print "[sys] Start automation..."
      global t
      GPIO.setup(40, GPIO.OUT)
      GPIO.output(40, 1)

      t = multiprocessing.Process(target=execute_js('ble-echo.js'))
      t.start()
#      subprocess.call('sudo node ble-echo.js' , shell=True)
#      pro = subprocess.Popen('sudo node ble-echo.js', stdout=subprocess.PIPE, 
#                       shell=True, preexec_fn=os.setsid) 
    if message == "stop":
      print "[sys] Stop automation..."
      t.terminate() 
#      subprocess.call('sudo node ble-echo.js' , shell=False)           
#      os.killpg(os.getpgid(pro.pid), signal.SIGTERM) 
    if message == "reboot":
      print "[sys] Reboot now..."
      os.system('sudo reboot -f')

    if message == "updateuser":
      print "[sys] Update user ..."
      self.update_user()      
    if "removeuser" in message:
      print "[sys] Remove user :" + message
      data = message.split(",")
      self.remove_user(data[1],data[2])
 
  def on_close(self):
    print '[WS] Connection was closed.'
    

application = tornado.web.Application([
  (r'/', MainHandler),
  (r'/ws', WSHandler),
  ], **settings)


if __name__ == "__main__":
    try:
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(PORT)
        main_loop = tornado.ioloop.IOLoop.instance()

        print "Tornado Server started"
        main_loop.start()
	print "ok"
    except:
        print "Exception triggered - Tornado Server stopped."
        GPIO.cleanup()

#End of Program
