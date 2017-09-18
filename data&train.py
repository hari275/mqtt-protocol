import cv2,os
import numpy as np
from PIL import Image
import time as t
detector=cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
recognizer = cv2.face.createLBPHFaceRecognizer()
path='dataset'

def data():
    cam = cv2.VideoCapture('http://192.168.1.13:8087/mjpeg')
    Id=input('enter your id')
    sampleNum=0
    while(True):
        
        ret, img = cam.read()
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = detector.detectMultiScale(gray, 1.2, 5)
        print('1')
        for (x,y,w,h) in faces:
            print('2')
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            
            #incrementing sample number 
            sampleNum+=1
            #saving the captured face in the dataset folder
            cv2.imwrite("dataSet/krish."+str(Id) +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])

            cv2.imshow('frame',img)
            
            
        #wait for 100 miliseconds 
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        # break if the sample number is morethan 20
        elif sampleNum>500:
            break
    cam.release()
    cv2.destroyAllWindows()
def trainer():
    def training(path):
        #get the path of all the files in the folder
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    #create empth face list
        face=[]
        #create empty ID list
        Ids=[]
        #now looping through all the image paths and loading the Ids and the images
        for imagePath in imagePaths:
            #loading the image and converting it to gray scale
            faceImage=Image.open(imagePath).convert('L')
            #Now we are converting the PIL image into numpy array
            faceNp=np.array(faceImage,'uint8')
            #getting the Id from the image
            Id=int(os.path.split(imagePath)[-1].split(".")[1])
            # Get the face from the training images
            faces = detector.detectMultiScale(faceNp)
            # Loop for each face, append to their respective ID
            for (x,y,w,h) in faces:
                # extract the face from the training image sample
                face.append(faceNp[y:y+h,x:x+w])
                print (Id)
                Ids.append(Id)
                cv2.imshow("training",faceNp)
                cv2.waitKey(10)
        return Ids, face
    Ids, faces= training(path)
    recognizer.train(faces,np.array(Ids))
    recognizer.save('train/train.yml')
    cv2.destroyAllWindows()
data()
t.sleep(5)
trainer()
    
    
    
