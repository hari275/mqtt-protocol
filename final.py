 
# Import OpenCV2 for image processing
import cv2
import numpy as np
import subprocess as s
import time as t
import os as o

# Create Local Binary Patterns Histograms for face recognization
recognizer = cv2.face.createLBPHFaceRecognizer()
recognizer.load('./train/train.yml')
cascade = "haarcascade_frontalface_alt.xml"
faceCascade = cv2.CascadeClassifier(cascade);


# Initialize and start the video frame capture
cam = cv2.VideoCapture('http://192.168.1.15:8087/mjpeg')

# Loop
while True:
    # Read the video frame
    ret, im =cam.read()

    # Convert the captured frame into grayscaleq
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

    # Get all face from the video frame
    faces = faceCascade.detectMultiScale(gray, 1.2,5)

    # For each face in faces
    for(x,y,w,h) in faces:

        # Create rectangle around the face
        cv2.rectangle(im, (x,y), (x+w,y+h), (0,255,0), 2)
        result = cv2.face.MinDistancePredictCollector()
        recognizer.predict(gray[y:y+h,x:x+w],result,0)
        Id = result.getLabel()
        conf = result.getDist()
        # Recognize the face belongs to which ID
        if (conf < 65):
        # Check the ID if exist 
            if(Id == 1):
                print("krish")
                s.Popen(['python2.7','./mqtt.py'])# start webpage
                t.sleep(300)
                o.system("pkill -f automate.py")# kill page
                
                
            #If not exist, then it is Unknown
        else:
           print("unknown")
           n=s.Popen(['python2.7','./fail.py'])
           t.sleep(300)
           o.system("pkill -f fail.py")

    

    



      
