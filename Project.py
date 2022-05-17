import time
from multiprocessing import Process
from stepper import stepperMotor
from SubProject import ultrasonicLcd
from lcd import lcd
from camera import camera

print("Waiting a few seconds for the sensor to settle down")
time.sleep(0.5)

#to use multiprocessing
if __name__=='__main__':
    stepper=Process(target=stepperMotor)
    ultrasonicLcd=Process(target=ultrasonicLcd)
    lcd=Process(target=lcd)
    # camera=Process(target=camera)
    
    ultrasonicLcd.start()
    stepper.start()
    lcd.start()
    # camera.start()    

    ultrasonicLcd.join()
    stepper.join()
    lcd.join()
    # camera.join()