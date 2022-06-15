from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html') # to render the index.html template

def gen():
    img = cv2.imread('wolf.jpg')
    img = cv2.resize(img, (0,0), fx=1.0, fy=1.0)
    frame = cv2.imencode('.jpg', img)[1].tobytes()
    yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(debug=True)




