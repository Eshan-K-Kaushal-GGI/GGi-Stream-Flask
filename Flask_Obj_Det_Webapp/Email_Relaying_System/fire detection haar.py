import numpy as np
import cv2
import time
import os
import datetime
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SUBJECT = 'Fire Please check'
TEXT = 'Please check for possible fire'
message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
Email_Stat = False
def send_email_function(image_path):
    recEmail = 'eshan5441@gmail.com'
    recEmail = recEmail.lower()
    with open(image_path, 'rb') as f:
        img_data = f.read()
    image = MIMEImage(img_data, name = image_path)
    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = 'eshan5441@gmail.com'
    msg['To'] = 'eshan5441@gmail.com'

    text = MIMEText("Test")
    msg.attach(text)
    msg.attach(image)

    try:
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.ehlo()
        server.starttls()
        server.login('eshan5441@gmail.com', 'Lordeshan@99')
        server.sendmail('eshan5441@gmail.com', recEmail, msg.as_string())
        print('sent')
        server.close()
    except Exception as e:
        print(e)

if not os.path.exists('detections'):
    os.mkdir('detections')

fire_cascade = cv2.CascadeClassifier('cascade.xml')
# cascade.xml is the classifier file that contains the parameters of classifier
# checks for fire detection

cap = cv2.VideoCapture(0)  # start video capturing

#cap = cv2.VideoCapture('rtsp://ADMIN:GGi1234!@24.7.16.134:554/stream1')
count = 0
frame = 1
frame_c = 0
cap.set(cv2.CAP_PROP_BUFFERSIZE, 60) # keep 60 frames in the buffer to prevent lags and glitches
while cap.isOpened():
    ret, img = cap.read()  # capture a frame
    #img = cv2.resize(img, (1200, 700))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert image to grayscale
    fire = fire_cascade.detectMultiScale(img, 12, 5)  # test for fire detection

    for (x, y, w, h) in fire:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # highlight the area of image with fire
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        if not os.path.exists('detections/' + 'Fire'):
            os.makedirs('detections/' + 'Fire')



        #print('Fire is detected..!' + str(count))
        count = count + 1
        time.sleep(0.1)  # wait

        if count % 10 == 1:
            print('Fire! Please Check!')
            print(count)

        cv2.imwrite(
            'detections/' + 'Fire' + '/' + str(count) + '.jpg',
            roi_color)

        if Email_Stat == False:
            send_email_function('detections/Fire/' + str(count)+ '.jpg')
            Email_Stat = True

    cv2.imshow('img', img)
    k = cv2.waitKey(100) & 0xff
    if k == 27 or k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()