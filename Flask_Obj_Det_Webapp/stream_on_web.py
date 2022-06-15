import cv2
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('Index_Stream.html') # to render the index.html template
#
# def gen():
#     cap = cv2.VideoCapture('rtsp://ADMIN:GGi1234!@24.7.16.134:554/stream1')
#
#     while(True):
#         ret, img = cap.read()
#         if ret==True:
#             img = cv2.resize(img, (0,0), fx=1.0, fy=1.0)
#             frame = cv2.imencode('.jpg', img)[1].tobytes()
#             yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#             #cv2.imshow('frame',frame)
#             #if cv2.waitKey(1) & 0xFF == ord('q'):
#         else:
#             break


def gen():

    cap = cv2.VideoCapture('rtsp://ADMIN:GGi1234!@24.7.16.134:554/stream1')
    # cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

    while True:
        ret, img = cap.read()
        if ret == True:
            img = cv2.resize(img, (1200, 720))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.112, 6, minSize=(
            25, 25))  # a scale factor and it determines the speed and accuracy of the algo
            bodies = body_cascade.detectMultiScale(gray, 1.112,
                                                   6)  # again the scale factor, the second argument is number of neighbors to be accepted for detection


            for (x, y, width, height) in faces:
                cv2.rectangle(img, (x, y), (x + width, y + height), (255, 0, 0), 3)
                face_roi = img[y:y + height, x:x + width]

            for (x, y, width, height) in bodies:
                cv2.rectangle(img, (x, y), (x + width, y + height), (255, 200, 0), 3)
                body_roi = img[y:y + height, x:x + width]

            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break


@app.route("/video_feed")
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
app.run(debug=True)
# cap.release()

# cv2.destroyAllWindows()