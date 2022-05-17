from flask import Flask, render_template, Response, request

# emulated camera
from camera import VideoCamera
import requests
import cv2, base64
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

lampRelay=26

GPIO.setup(lampRelay, GPIO.OUT)
GPIO.output(lampRelay, GPIO.LOW)

app = Flask(__name__)


@app.route('/camera')
def index():
    # Video streaming home page.
    return render_template('index.html')


def gen(camera):
    # Video streaming generator function 
    while True:
        data = camera.get_frame()
        # frame = camera.get_frame()
        frame=data[0]
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame +  b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

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


    # lampStatus = GPIO.input(lampRelay)
    # templateData = {
    #     'lamp'  : lampStatus
    #     }
    return render_template('index.html')
    # return render_template('index.html', **templateData)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True)