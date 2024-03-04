# Pi-in-the-Sky

&nbsp;

# `Table of Contents`
* [Planning](#planning)
* [Coding](#coding)
* [Wiring](#wiring)
* [Building A Prototype](#building_a_prototype)

&nbsp;
# `Planning`
[Link to planning Document](https://docs.google.com/document/d/14-PHrZZvjooZSPuYYvAT_kGfdMwqDnR2ftNQUhQHIGQ/edit)

The plans changed quite frequently, as we found some designs better than others, or decided to scrap some ideas entirely, but I'll get into that in other sections.

# `Coding`
The main idea for our design was partially based on the fact that neither of us either excelled at code or wanted to be the one to write it all, so we made sure the code was almost entirely comprised of things we knew how to do. I'll go through it in chunks.

```python
#type:ignore

import adafruit_mpu6050
import adafruit_mpl3115a2
import busio
import time
import board
from digitalio import DigitalInOut, Direction

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
red = DigitalInOut(board.GP16)
red.direction = Direction.OUTPUT 

sda_pin = board.GP14
scl_pin = board.GP15
i2c = busio.I2C(scl_pin, sda_pin)
mpu = adafruit_mpu6050.MPU6050(i2c, address=0x68) 
#the setup soup
prev=0
deg=0
```
All of this is just the imports and Pico pin setup, aptly titled "the setup soup". I'll only refer to it as such from now on. The "#type:ignore" is just so it doesn't spit out problems that don't actually exist, because otherwise it complained about every single import despite it all working fine.

```python
with open("/data.csv", "a") as datalog: #the thing that allows the data to be Grabbed
    while True: #the Loop
```
These two lines open up an excel sheet named data.csv, which is where all of the outputs will go, and also set up The Loop, which is the rest of the code.

```python
        prev = deg
        deg=(round(float(mpu.gyro[0]), 1)*(0.2)*(180/3.14159))+prev #converting radians/second into just degrees
```
These two lines caused a lot of pain. The idea is that every time the code runs through the loop, it sets the previous degrees variable to what the degrees variable was the last time, to store it. The new angle, which would be the difference between the current angle and the previous angle, is then calculated and added to the previous one. This SHOULD create an accurate way to keep track of the angle. However, since the gyroscope measures angle in radians per second, we have to convert it to static degrees. Thats what the 180/pi, and the 0.2 (the time it SHOULD take to loop once) are for. As evidenced by my use of the word SHOULD, it did not do this. Despite having done this exact code in a project from last year (i even copied the code), it just didn't work for reasons I would discover later.(later pending)

I also wanted to keep track of the height the payload was at, but the altimeter cause a lot of wiring and code pain, so I scrapped it to save my sanity.
```python
        acc = mpu.acceleration
        h = mpl.altitude #shorter variables
        print("X = ["+str(acc[0])+"]| Y = ["+str(acc[1])+"]| Z = ["+str(acc[2])+"]| ANGLE = ["+str(deg)+"]") #prints acceleration values using the archaic str() method
        if acc[2] <= 0:
            red.value = True #if number small light go
            tilt=1
        else:
            red.value = False #if number big light no
            tilt=0
```

# `Wiring`


# `Building A Prototype`


