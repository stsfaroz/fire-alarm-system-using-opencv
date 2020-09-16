# camera.py
#F1YbN3SwfHKjFL0puCd2sAcPgC6SBFYNV32EsUgd
import cv2
import PIL.Image
from PIL import Image
from twilio.rest import Client as TwilioRestClient


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = ''
auth_token = ''
whatsapp = TwilioRestClient(account_sid, auth_token)





TWILIO_PHONE_NUMBER = ""

DIAL_NUMBERS = [""]

TWIML_INSTRUCTIONS_URL = \
  "http://static.fullstackpython.com/phone-calls-python.xml"

client = TwilioRestClient(account_sid,auth_token)

def dial_numbers(numbers_list):
    for number in numbers_list:
        print("Dialing " + number)
        client.calls.create(to=number, from_=TWILIO_PHONE_NUMBER,url=TWIML_INSTRUCTIONS_URL, method="GET")
class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        self.g=0
          
        
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        suc, img = self.video.read()

 
        fire_cascade = cv2.CascadeClassifier('fire_detection.xml')

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        fire = fire_cascade.detectMultiScale(img, 1.2, 5)
        for (x,y,w,h) in fire:
            v=fire[0][0]
            print("fire is detected",v)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            print('Fire is detected..!')
            dial_numbers(DIAL_NUMBERS)
            print("calling.......")
            message = whatsapp.messages.create(
                              body='Fire is detected!!!',
                              from_='whatsapp:+14155238886',
                              to='whatsapp:+916381892510'
                          )

        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
