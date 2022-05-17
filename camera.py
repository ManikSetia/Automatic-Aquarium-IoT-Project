

from inspect import currentframe
from flask import Flask, render_template, Response
import cv2
import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

lampRelay=26

GPIO.setup(lampRelay, GPIO.OUT)
GPIO.output(lampRelay, GPIO.LOW)


app=Flask(__name__)
camera=cv2.VideoCapture(0)

def generateFrames():
    while True:

        #read the camera frame
        success, frame=camera.read()
        if not success:
            break
        else:
            ret, buffer=cv2.imencode('.jpg', frame)
            frame=buffer.tobytes()
        
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame +  b'\r\n')


@app.route('/')
def index():
        # currentTime = datetime.now().strftime("%H:%M:%S")
        # time={'currentTime':currentTime}
        # return render_template("index.html", **time)
    GPIO.output(lampRelay, GPIO.HIGH)
    return render_template("home.html")

@app.route('/video')
def video():
    return Response(generateFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    if deviceName == 'lamp':
        actuator = lampRelay
    if action == "on":
        GPIO.output(actuator, GPIO.LOW)

    elif action == "off":
        GPIO.output(actuator, GPIO.HIGH)

    elif action == "delay":
        #turn on the lamp for 15 minutes
        GPIO.output(actuator, GPIO.LOW)
        time.sleep(900)
        GPIO.output(actuator, GPIO.HIGH)

    return render_template('index.html')
    # return render_template('index.html', **templateData)

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=False, threaded=True)
