from email.message import EmailMessage
import face_recognition
import cv2 
# import pyttsx3
import datetime
import gtts
import time
# from playsound import playsound
import smtplib
import imghdr
import os
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import requests
import re
import multiprocessing

class project:
            
    def image(self):
        '''Only For Knowledge'''
        image = face_recognition.load_image_file('obama.png')
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(image)
        for i in range(len(face_locations)):
            cv2.rectangle(image,(face_locations[i][3],face_locations[i][0]),(face_locations[i][1],face_locations[i][2]),(255, 0, 0),2)
        cv2.imshow('obama.png',image)
        cv2.waitKey(0)

    def image_saver(self):
        try:
            video = cv2.VideoCapture(0)
            check,frame = video.read()
            cv2.imwrite('./temp/savedImage.jpg',frame)
            video.release()
        except:
            print('WebCam Is Not Working Properly or Plugged In.')

    def ngrok(self):
        os.system('ngrok http 5000 --region=in > /dev/null')

    def flask_app(self):
        os.system('flask run > /dev/null')
        
    def url_saver(self):
        url = os.popen('curl -s localhost:4040/api/tunnels | jq .tunnels[0].public_url').read()
        with open('link.txt','w') as file:
            file.write(url)
            file.close()
        
        
    def email(self):
        EMAIL_ADDRESS = os.environ.get('email_address')
        EMAIL_PASSWORD = os.environ.get('email_password')
        msg = EmailMessage()
        msg['Subject'] = 'Intruder Alert!'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        process1 = multiprocessing.Process(target=self.ngrok)
        process2 = multiprocessing.Process(target=self.flask_app)
        process3 = multiprocessing.Process(target=self.url_saver)
        process1.daemon = True
        process1.start()
        time.sleep(5)
        process2.daemon = True
        process2.start()
        process3.daemon = True
        process3.start()
        time.sleep(5) 
        url = None
        with open('link.txt','r') as file:
            url = file.read()
        msg.set_content(f'Do You want to Allow person/persons to Enter?\n{url}')
        files = ['./temp/savedImage.jpg']
        for file in files:
            with open(file,'rb') as f:
                file_data = f.read()
                file_name = f.name
                file_type = imghdr.what(f.name)
            msg.add_attachment(file_data,maintype='image',subtype=file_type,filename=file_name)
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
            smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
            smtp.send_message(msg)
        with open('response.txt','w'):
            pass
        t=30
        while(t):
            t-=1
            if(os.path.getsize('response.txt')==1):
                f = open("response.txt", "r")
                var = f.read()
                process1.kill()
                process2.kill()
                process3.kill()
                os.system('pkill -9 ngrok')
                os.system('pkill -9 flask')
                return True if var=='1' else False 
            time.sleep(1)
        process1.kill()
        process2.kill()
        process3.kill()
        os.system('pkill -9 ngrok')
        os.system('pkill -9 flask')
        return False

    def recogonizer(self):
        train_images = os.listdir('./images/')
        train_images_path = ['./images/'+ x for x in train_images]
        imgTest = face_recognition.load_image_file('./temp/savedImage.jpg')
        imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)
        encodeFace = face_recognition.face_encodings(imgTest)[0]
        for i in train_images_path:
            imgTrain = face_recognition.load_image_file(i)
            encodeListKnown = face_recognition.face_encodings(imgTrain)[0]
            matches = face_recognition.compare_faces([encodeListKnown],encodeFace)
            faceDis = face_recognition.face_distance([encodeListKnown],encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                return True
            else:
                return False
            
    def webcam(self):
        '''Detecting Webcam and Making Rectangles on it.'''
        try:
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            video = cv2.VideoCapture(0)
            while True:
                check,frame = video.read()
                faces = face_cascade.detectMultiScale(
                    frame
                )
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.putText(frame,'Be Inside The Frame',(40,35),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),3)
                cv2.imshow('Video',frame)
                if cv2.waitKey(1)==ord('q'):
                    video.release()
                    cv2.destroyAllWindows()
                    self.image_saver()
                    break 
        except:
            print('WebCam Is Not Working Properly or Plugged In.')
            
    def greeting(self):
        curr_time = datetime.datetime.now()
        curr_time = str(curr_time.hour).zfill(2)+str(curr_time.minute).zfill(2)
        if(curr_time>'0000' and curr_time<='1159'):
            self.speak('Good Morning')
        elif(curr_time<='1700'):
            self.speak('Good AfterNoon')
        else:
            self.speak('Good Evening')

    def speak(self,saying):
        tts = gtts.gTTS(saying)
        tts.save('./temp/voice.mp3')
        sound = AudioSegment.from_mp3("./temp/voice.mp3")
        play(sound)
        
    def autodetect(self):
        try:
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            video = cv2.VideoCapture(0)
            while True:
                check,frame = video.read()
                faces = face_cascade.detectMultiScale(
                    frame
                )
                if(len(faces)==0):
                    return False
                else:
                    return True
        except:
            print('WebCam Is Not Working Properly or Plugged In.')
            
    def main(self):
        while(True):
            if(self.autodetect()):
                self.greeting()
                self.speak('hi i am virtual assisstant')
                time.sleep(5)
                self.webcam()
                if not self.recogonizer():
                    self.speak('oops i am unable to detect you asking owner to verify')
                    if self.email()==True:
                        self.speak('You Can Go Inside the House')
                    else:
                        self.speak('You are Not Allowed to Go inside')
                else:
                    self.speak('You Can Go Inside the House')
                    
                time.sleep(30)
            else:
                time.sleep(1)
            
if __name__ == '__main__':
    obj = project()
    obj.main()
