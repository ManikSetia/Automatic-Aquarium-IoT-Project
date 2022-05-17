import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

def stepperMotor():

    PIN=[16, 12, 13, 21]

    forwardButton=20
    backwardButton=25

    GPIO.setup(forwardButton, GPIO.IN)
    GPIO.setup(backwardButton, GPIO.IN)

    forwardSequence=[
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

    backwardSequence=[
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0]
    ]

    # forwardSequence=[
    #     [1, 0, 0, 0],
    #     [1, 1, 0, 0],
    #     [0, 1, 0, 0],
    #     [0, 1, 1, 0],
    #     [0, 0, 1, 0],
    #     [0, 0, 1, 1],
    #     [0, 0, 0, 1],
    #     [1, 0, 0, 1]
    # ]

    # backwardSequence=[
    #     [1, 0, 0, 1],
    #     [1, 0, 0, 1],
    #     [0, 0, 0, 1],
    #     [0, 0, 1, 1],
    #     [0, 0, 1, 0],
    #     [0, 1, 1, 0],
    #     [0, 1, 0, 0],
    #     [1, 1, 0, 0],
    #     [1, 0, 0, 0]
    # ]

    for pin in PIN:
        GPIO.setup(pin, GPIO.OUT)

    try:
        
        # We are using LOW ACTIVE INPUT for switches, which means when button is pressed signal on the input becomes low voltage

        while 1:
            if(GPIO.input(forwardButton) == GPIO.LOW):
                print("MANUAL: Rotate feeder right")
                for singleStepping in range(4):
                    for pin in range(4):
                        GPIO.output(PIN[pin], forwardSequence[singleStepping][pin])
                    
                    time.sleep(0.01)

            if(GPIO.input(backwardButton) == GPIO.LOW):
                print("MANUAL: Rotate feeder left")
                for singleStepping in range(4):
                    for pin in range(4):
                        GPIO.output(PIN[pin], backwardSequence[singleStepping][pin])
                        
                    time.sleep(0.01)
        
    except KeyboardInterrupt:
        GPIO.cleanup()

# stepperMotor()