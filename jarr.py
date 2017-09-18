import subprocess as s
import time as t
import os as o
while True:
    ##open a jar file
    p = s.Popen(['java -jar CloudCamStreamServer.jar 192.168.1.15 8089 8087'],shell=True,stdout=s.PIPE,stderr=s.PIPE,bufsize=1)
    def jarrprocess():
        
        for line in iter(p.stdout.readline, b''):# check for connection from the phone
            print (line)
            if(line==b'Received a new connection from CloudCam.\n'):
                s.Popen(['python','./final.py'])#detection program
                t.sleep(420)#clode the program after 7 minutes
                o.system("pkill -f final.py")#kill to restart program
                t.sleep(30)
                
                jarrprocess()
                
    while True:
        jarrprocess()
            
   
      
