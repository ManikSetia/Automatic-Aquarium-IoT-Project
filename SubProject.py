#For LCD
import cgitb; cgitb.enable()
import busio
import digitalio
import board
from adafruit_bus_device.spi_device import SPIDevice
import adafruit_pcd8544
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import RPi.GPIO as GPIO
import time
from datetime import datetime
from stepper import stepperMotor
from multiprocessing import Process
import requests


def ultrasonicLcd():

    GPIO.setwarnings(False)

    # credentials to send data to the gateway
    url="http://tarupi.hub.ubeac.io/iotesstarupi"
    uid="iotestarupi"

    #to disable warnings
    GPIO.setwarnings(False)

    #Setting pins for ultrasonic sensor
    trig=4
    echo=27

    #pins for buttons
    waterPumpSwitch=22
    lampSwitch=5
    
    #pins for relay
    waterPumpRelay=19
    lampRelay=26

    #for lampSwitch so that it gets ON at alternative times
    counterLampRelay=True

    #to see lamp is ON or OFF
    lampStatus="OFF"

    #to check if pump is activated or not
    pumpStatus="OFF"

    GPIO.setmode(GPIO.BCM)

    #Setting TRIG of ultrasonic sensor to output and ECHO to input
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)

    #Setting all switches to input mode
    GPIO.setup(waterPumpSwitch, GPIO.IN)
    GPIO.setup(lampSwitch, GPIO.IN)
    

    #Initially, setting all pins for relay to HIGH voltage
    GPIO.setup(waterPumpRelay, GPIO.OUT)
    GPIO.setup(lampRelay, GPIO.OUT)
    GPIO.output(waterPumpRelay, GPIO.HIGH)
    GPIO.output(lampRelay, GPIO.HIGH)


    try:
        while 1:
            #Ultrasonic sensor
            
            # Give 10 microseconds pulse to TRIG so that it can send ultrasonic wave of 8 burst cycles
            GPIO.output(trig, GPIO.HIGH)
            time.sleep(0.000001)
            GPIO.output(trig, GPIO.LOW)

            # Now wait until ECHO pin goes high
            while(GPIO.input(echo) == GPIO.LOW):
                pass

            # Now ECHO pin is HIGH, start noting the time, we've sent the signal
            startTime=time.time()

            # Now wait until ECHO pin is HIGH
            while(GPIO.input(echo) == GPIO.HIGH):
                pass

            # Now ECHO is LOW, stop the time, we've received the signal
            stopTime=time.time()

            timeTaken=stopTime-startTime
            distance=timeTaken*17000            
            print("Distance: ", round(distance, 2), "cm")

            #to activate the pump when water level decreases and the distance between the water level and the sensor is more than 10 cm.
            if(round(distance, 2)<10.00):
                pumpStatus="ON"
                print("Pump: ON")
                GPIO.output(waterPumpRelay, GPIO.LOW)


            # We are using LOW ACTIVE INPUT for switches, which means when button is pressed signal on the input becomes low voltage
            
            #For water pump (as long as button is pressed, it works)
            elif(GPIO.input(waterPumpSwitch) == GPIO.LOW):
                print("Water pump switch pressed / water pump is activated")
                pumpStatus="ON"
                print("Pump: ON")
                GPIO.output(waterPumpRelay, GPIO.LOW) #water pump is activated

            #For lamp (when button is pressed, it goes ON. Again when it is pressed, it goes OFF)
            elif(GPIO.input(lampSwitch) == GPIO.LOW and counterLampRelay):
                print("Lamp switch pressed / Lamp is ON")
                lampStatus="ON"
                GPIO.output(lampRelay, GPIO.LOW) #lamp is activated
                counterLampRelay=False #so that we can turn off lamp in the next iteration
            
            #for turning off the lamp
            elif(GPIO.input(lampSwitch) == GPIO.LOW and not counterLampRelay):
                print("Lamp switch pressed again / Lamp is OFF")
                lampStatus="OFF"
                GPIO.output(lampRelay, GPIO.HIGH)
                counterLampRelay=True

            else:
                # print("Button not pressed")
                GPIO.output(waterPumpRelay, GPIO.HIGH)
                pumpStatus="OFF"
                print("Pump: OFF")


            time.sleep(1) #display output after every second

            #sending data to the gateway
            data={
                "id": uid,
                "water depth":str(round(distance, 2))+' cm',
                "Light status":lampStatus,
                "Pump status":pumpStatus
            }
            requests.post(url, verify=False, json=data)
            
    except KeyboardInterrupt:
        GPIO.cleanup()

# ultrasonicLcd()