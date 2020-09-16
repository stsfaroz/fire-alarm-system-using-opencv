

from flask import Flask, render_template, request ,Response, session
app = Flask(__name__)
app.secret_key = 'any random string'
app.config['TEMPLATES_AUTO_RELOAD'] = True
import os
import numpy as np
import cv2
import  imutils
import pytesseract
import pandas as pd
from camera import VideoCamera


APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/home',methods=["GET", "POST"])
def home():
   return render_template('home.html')

@app.route('/index',methods=["GET", "POST"])
@app.route("/")

def index():
   return render_template('index.html')

@app.route('/result',methods=["GET", "POST"])
def result():
    if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            session['username'] = password
            if username=="admin" and password=="admin":
                return render_template("result.html",result=username)
            else:
                return render_template("index.html",result="wrong username or password")

@app.route("/logout")         
def logout():
  session.pop('username', None)
  return render_template('index.html')

def gen(camera):
    
    while True:
        frame = camera.get_frame()
        
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
        

def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




TEMPLATES_AUTO_RELOAD = True


if __name__ == '__main__':
   app.run(debug = True)













































import numpy as np      # For efficient utilization of array
import cv2          # Computer vision library
import os         # Here this package is used writing CLI commands
import vlc_ctrl
import time 
import os     # package used for controlling vlc media player
import subprocess
import tkinter as tk
from tkinter import filedialog as fd
root = tk.Tk()
def write_slogan():
  global filename
  filename = fd.askopenfilename()
def play():
  cap = cv2.VideoCapture(0)   
  os.system("vlc-ctrl play -p "+filename)

  # Frontal face classifier is imported here
  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
  import numpy as np
  import cv2
  import math

#LOADING HAND CASCADE
  hand_cascade = cv2.CascadeClassifier('Hand_haar_cascade.xml')


  # Flag is used to pause and play the video [ if flag is 1 then the video plays else it doesn't ]
  Pauseflag = 0 

  try:
    while True:
      ret , img = cap.read() # For caturing the frame 
      blur = cv2.GaussianBlur(img,(5,5),0) # BLURRING IMAGE TO SMOOTHEN EDGES
      grayh = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY) # BGR -> GRAY CONVERSION
      retval2,thresh1 = cv2.threshold(grayh,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) # THRESHOLDING IMAGE
      hand = hand_cascade.detectMultiScale(thresh1, 1.3, 5) # DETECTING HAND IN THE THRESHOLDE IMAGE
      mask = np.zeros(thresh1.shape, dtype = "uint8") # CREATING MASK
      for (x,y,w,h) in hand: # MARKING THE DETECTED ROI
        cv2.rectangle(img,(x,y),(x+w,y+h), (122,122,0), 2) 
        cv2.rectangle(mask, (x,y),(x+w,y+h),255,-1)
      img2 = cv2.bitwise_and(thresh1, mask)
      final = cv2.GaussianBlur(img2,(7,7),0)  
      contours, hierarchy = cv2.findContours(final, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

      cv2.drawContours(img, contours, 0, (255,255,0), 3)
      cv2.drawContours(final, contours, 0, (255,255,0), 3)

      if len(contours) > 0:
        cnt=contours[0]
        hull = cv2.convexHull(cnt, returnPoints=False)
        # finding convexity defects
        defects = cv2.convexityDefects(cnt, hull)
        count_defects = 0
        # applying Cosine Rule to find angle for all defects (between fingers)
        # with angle > 90 degrees and ignore defect

        if not (defects is None):
          for i in range(defects.shape[0]):
            p,q,r,s = defects[i,0]
            finger1 = tuple(cnt[p][0])
            finger2 = tuple(cnt[q][0])
            dip = tuple(cnt[r][0])
            # find length of all sides of triangle
            a = math.sqrt((finger2[0] - finger1[0])**2 + (finger2[1] - finger1[1])**2)
            b = math.sqrt((dip[0] - finger1[0])**2 + (dip[1] - finger1[1])**2)
            c = math.sqrt((finger2[0] - dip[0])**2 + (finger2[1] - dip[1])**2)
            # apply cosine rule here
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57.29
            # ignore angles > 90 and highlight rest with red dots
            if angle <= 90:
                count_defects += 1
        # define actions required
        if count_defects == 1:
          print("2")
          subprocess.Popen(['vlc-ctrl',  'volume',  '-0.1'])
          #cv2.putText(img,"THIS IS 2", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 2:
          print("3")
          subprocess.Popen(['vlc-ctrl',  'volume',  '-0.1'])
          #cv2.putText(img, "THIS IS 3", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 3:
          print("4")
          subprocess.Popen(['vlc-ctrl',  'volume',  '+10%'])
          #cv2.putText(img,"This is 4", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif count_defects == 4:
          print("5")
          subprocess.Popen(['vlc-ctrl',  'volume',  '+10%'])
          #cv2.putText(img,"THIS IS 5", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)



      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Gets the x and y coordinates of the face as well the width and height of the face if detected 
      for (x, y, w, h) in faces:
        print ("Face is facing front")
        time.sleep(3)

        os.system("vlc-ctrl play")
        time.sleep(3)
        Pauseflag = 1 # Face is detected hence play the video continuesly

      if Pauseflag == 0: # Face is not facing front hence pause the video

        print ("Face is not facing front")
        ti=time.asctime()
        m=ti[14:16]
        s=ti[17:19]
        mi=int(m)
        si=int(s)
        print(mi,si)
        os.system("vlc-ctrl pause")
        if mi==59:
          mi=00
        else:
          co=mi+1
        cs=si
        if mi==co and si==cs:
          os.system("systemct1 suspend")


          
        
        
    
      
      Pauseflag = 0 

  except KeyboardInterrupt:
    print ("Closing the application!!! [Interrupted]") 

  cap.release() 
    

    

tk.Entry(root, width = 55).grid(row=0, column=0)

tk.Button(root, text = "Generate",command=write_slogan).grid(row=1, column=0, pady = (0,50))

tk.Button(root, text = "play",command=play).grid(row=2, column=0)

tk.Button(root, text = "quit",command=quit).grid(row=4, column=0)
root.mainloop()