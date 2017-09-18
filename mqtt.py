import time as t                                                                    
from itertools import cycle                                                     
from flask import Flask, render_template,request, redirect,url_for
import random as r
import paho.mqtt.client as m
from flask_socketio import SocketIO as s
import RPi.GPIO as GPIO
import urllib2 as u
app = Flask(__name__)
mc=m.Client()
mc.connect("localhost",1883,60)
mc.loop_start()
pins = {
    2 : {'name' : 'light1','topic':'esp8266/2','state' : False},
    3 : {'name' : 'light2','topic':'esp8266/3', 'state' : False}
   }
templateData = {
   'pins' : pins
   }

PIN_NUM1 = 7
PIN_NUM = 11
PIN_NUM2 = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_NUM,GPIO.OUT)
GPIO.setup(PIN_NUM1,GPIO.OUT)
GPIO.setup(PIN_NUM2,GPIO.OUT)
state_cycle = cycle(['lock', 'unlock'])
def endcode():
    GPIO.output(PIN_NUM1,False)
    GPIO.output(PIN_NUM2,False)
    GPIO.output(PIN_NUM,False)
x= r.randint(1000,9999)
y='https://smsapi.engineeringtgr.com/send/?Mobile=7418817375&Password=q1w2e3r4t5y6&Message='+str(x)+'&To=7418817375'
u.urlopen(y)
print(x)
pwd=x

@app.route("/<pwd>/")
def main(pwd):
    return render_template('main2.html')
@app.route("/<pwd>/room")
def room(pwd):
   templateData = {
   'pins' : pins,'pwd':pwd
   }
    
   return render_template('main3.html', **templateData)
#@app.route("/<pwd>/room/<changePin>/<action>")
@app.route("/<pwd>/<changePin>/<action>")
def action(pwd,changePin,action):
    changePin = int(changePin)
    deviceName = pins[changePin]['name']
    
    
    if action == "1" :
        mc.publish(pins[changePin]['topic'],"1")
        pins[changePin]['state'] = 'True'
       
        
        
        
    if action == "0":
        mc.publish(pins[changePin]['topic'],"0")
        pins[changePin]['state'] = 'False'
    templateData = {
        'pins' : pins,'pwd':pwd
         }
    return render_template('main3.html', **templateData)
    
@app.route("/<pwd>/<state>")
def lockstate(pwd,state=None): 
   if (state == 'lock'):
      GPIO.output(PIN_NUM,True)
      GPIO.output(PIN_NUM1,True)
      GPIO.output(PIN_NUM2,False)
      t.sleep(2)
      ##raw_input("Press Enter to stop:")
      endcode()
      GPIO.cleanup()
      print("locked")
   

   if (state =='unlock'):
      GPIO.output(PIN_NUM,True)
      GPIO.output(PIN_NUM1,False)
      GPIO.output(PIN_NUM2,True)
      t.sleep(2)
      ##raw_input("Press Enter to stop:")
      endcode()
      GPIO.cleanup()
      print("unlocked")
   
   template_data = {                                                           
        'title' : state,                                                    
   }
   
   return render_template('main5.html', **template_data)
       

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        
        if (request.form['password']!= str(x)):
           error='invaild creditials'
        else:
            #return redirect(url_for('main',pwd=str(x)))
            return redirect(url_for('main'))
            
    return render_template('main1.html')

if __name__ == "__main__":                                                      
    app.run(host='192.168.1.15', port=80,debug = True)
