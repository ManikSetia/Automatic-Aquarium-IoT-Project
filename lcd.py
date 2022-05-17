def lcd():
    import cgitb; cgitb.enable()
    import busio
    import digitalio
    import board
    from adafruit_bus_device.spi_device import SPIDevice
    import adafruit_pcd8544
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
    import time
    import RPi.GPIO as GPIO
    from datetime import datetime

    #for lampSwitch so that it gets ON at alternative times
    # counterLampRelay=True
    lampSwitch=5
    lampRelay=26


    #Setting pins for ultrasonic sensor
    trig=4
    echo=27

    #Setting TRIG of ultrasonic sensor to output and ECHO to input
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)

    GPIO.setup(lampSwitch, GPIO.IN)
    GPIO.setup(lampRelay, GPIO.OUT)


    def getWaterDepth():
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

            return distance

    def getLampStatus():
        lampStatus=GPIO.input(lampRelay)
        if(lampStatus):
            print("Lamp: OFF")
            return "OFF"
        print("Lamp: ON")
        return "ON"


    def getCountDown():

        def dateDiffInSeconds(date1, date2):
                timedelta = date2 - date1
                return timedelta.days * 24 * 3600 + timedelta.seconds

        def daysHoursMinutesSecondsFromSeconds(seconds):
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)
            global nextFeeding
            nextFeeding=(days, hours, minutes, seconds)
            return nextFeeding

        req = datetime.strptime('2022-05-17 11:58:00', '%Y-%m-%d %H:%M:%S')
        now = datetime.now()

        while req>now:
            print("Next feeding: %dd %dh %dm %ds" % daysHoursMinutesSecondsFromSeconds(dateDiffInSeconds(now, req)))
            countdown="%dd %dh %dm %ds" % daysHoursMinutesSecondsFromSeconds(dateDiffInSeconds(now, req))
            time.sleep(1)
            now = datetime.now()
            
            return countdown


    #LCD:
    #setting the pins according to the spi pins we used on the board
    spi=busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # setup for LCD, initialize the display
    dc=digitalio.DigitalInOut(board.D23) #data/command
    cs1=digitalio.DigitalInOut(board.CE1) #chip select CE1 for display
    reset=digitalio.DigitalInOut(board.D24) #reset
    display=adafruit_pcd8544.PCD8544(spi, dc, cs1, reset, baudrate=1000000)

    display.bias=4
    display.contrast=38
    display.invert=True

    # clear the display 
    display.fill(0)
    display.show()

    #default font
    font=ImageFont.load_default()
    secondFont=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 10)


    try:
        while 1:
            # get drawing object to draw on image
                image=Image.new('1', (display.width, display.height))
                draw=ImageDraw.Draw(image)

                # draw a white filled box to clear the image
                draw.rectangle((0,0,display.width, display.height), outline=255, fill=255)

                #getting current time from datetime object
                currentTime = datetime.now().strftime("%H:%M:%S")
                print("Current time: ", currentTime)


                #displaying output on the LCD
                draw.text((1,-2), str(currentTime))
                draw.text((1,6), 'Lamp:'+getLampStatus(), font=font)
                draw.text((1,16), 'Water depth:', font=secondFont)
                draw.text((1,22), str(round(getWaterDepth(), 2))+' cm', font=font)
                draw.text((1,32), 'Next feeding time:', font=secondFont)
                draw.text((1,38), getCountDown())
                
                display.image(image)
                display.show()

                print() #to print new line for better readability

    except KeyboardInterrupt:
        GPIO.cleanup()