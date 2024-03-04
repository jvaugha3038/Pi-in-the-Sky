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

```python:
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

```python:
with open("/data.csv", "a") as datalog: #the thing that allows the data to be Grabbed
    while True: #the Loop
```
These two lines open up an excel sheet named data.csv, which is where all of the outputs will go, and also set up The Loop, which is the rest of the code.

# `Wiring`


# `Building A Prototype`


