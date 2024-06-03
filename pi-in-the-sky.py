#type:ignore

import adafruit_mpu6050
import busio
import time
import board
from digitalio import DigitalInOut, Direction #the stuff again

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
red = DigitalInOut(board.GP16)
red.direction = Direction.OUTPUT 

sda_pin = board.GP14
scl_pin = board.GP15
i2c = busio.I2C(scl_pin, sda_pin)
mpu = adafruit_mpu6050.MPU6050(i2c, address=0x68) 
prev=0
deg=0
s=0.2
#the setup soup
def data(s):
    global prev
    global deg
    global acc
    
    prev = deg
    deg=((round(float(mpu.gyro[0]) +0.08, 1)*(s)*(180/3.14159)))+prev #converting radians/second into just degrees
    
    print("_________")
    
    acc = mpu.acceleration #shorter variable
    print("X = ["+str(acc[0])+"]| Y = ["+str(acc[1])+"]| Z = ["+str(acc[2])+"]| ANGLE = ["+str(deg)+"]") #prints acceleration values using the archaic str() method
    if acc[2] <= 0:
        red.value = True #if number small light go
        tilt=1
    else:
        red.value = False #if number big light no
        tilt=0
    return [tilt,deg]
            
with open("/data.csv", "a") as datalog: #the thing that allows the data to be Grabbed
    while True: #the Loop
        tilt, deg = data(s)
        t=time.monotonic()
        datalog.write(f"{t},{acc[0]},{acc[1]},{acc[2]},{tilt},{deg}\n") #the format of each line in the data table, using the better f string method
        led.value = True #blink when data is saved
        time.sleep(s) #wait
        datalog.flush()
        led.value = False