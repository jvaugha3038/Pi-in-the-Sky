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

The plans changed quite frequently, as we found some designs better than others, or decided to scrap some ideas entirely, but I'll get into that in relevant sections.

# `Coding`
The main idea for our design was partially based on the fact that neither of us either excelled at code or wanted to be the one to write it all, so we made sure the code was almost entirely comprised of things we knew how to do. By that I mean that the project code is essentially an altered version of my code for a previous assignment. I'll go through it in chunks.

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
All of this is just the imports and Pico pin setup, aptly titled "the setup soup". I'll only refer to it as such from now on. The "#type:ignore" is just so it doesn't spit out problems that don't actually exist, because otherwise it complains about every single import despite it all working fine.

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

I also wanted to keep track of the height the payload was at, but the altimeter caused a lot of wiring and code pain and output horribly inconsistent numbers, so I scrapped it to save my sanity.

```python
        acc = mpu.acceleration
        h = mpl.altitude #shorter variables
        print("X = ["+str(acc[0])+"]| Y = ["+str(acc[1])+"]| Z = ["+str(acc[2])+"]| ANGLE = ["+str(deg)+"]")
        #prints acceleration values using the archaic str() method
        if acc[2] <= 0:
            red.value = True #if number small light go
            tilt=1
        else:
            red.value = False #if number big light no
            tilt=0
```
THe first two lines just shorten the two sensors (the latter of which is obsolete now) into tiny variables for readability. The third line prints out all of the sensor variables for testing. The lines below simply light up an LED when its tilted sideways, which is a remnant of my older code that this is based on. I'm considering removing the LED and keeping just the variable itself.

```python
        t=time.monotonic()
        datalog.write(f"{t},{acc[0]},{acc[1]},{acc[2]},{tilt},{deg}\n") #the format of each line in the data table, using the better f string method
        led.value = True #blink when data is saved
        time.sleep(0.2) #wait
        datalog.flush()
        led.value = False 
```
The final chunk starts with another shorthand variable, which I've already talked about. The second line is the line that takes all of the important output variables and copies them into the excel sheet from earlier. Then, it blinks the Pico's onboard LED for a specific amount of time, and then the loop repeats.

The final code file itself may end up looking different from this breakdown (more polished, probably,) but this is how the code works, regardless of how it looks later.

# `Wiring`
The initial wiring consisted of an LED, a switch, the battery, the gyroscope/accelerometer, and the altimeter. Then I cut the altimeter out because I anticipated that I would have gone insane trying to wire all of this together on the far-too-small PiCowbell, which is what we had to use. Despite my precautions, I still lost my mind. 

## `Soldering`
This subsection exists because I made one fatal error that would then waste almost two weeks of time; daring to be one of the first people in the class to solder headers onto the PiCowbell, instead of waiting for someone else to do it correctly and learning off of them. The PiCowbell is essentially a more compact and practical prototype shield, but it required soldering wires onto it as opposed to using jumper wires. My mistake was soldering headers onto nearly every pin in the workspace in the middle of the board, which, plus the power and ground sections as well as the ~40 headers that would connect the Pico to the PiCowbell, led to over 100 pins to solder and hours of sadness. Most of it was mindless busywork until I was then told that I didn't need to do all of that, because I could've just soldered wires straight onto the board.
![pain](https://github.com/jvaugha3038/Pi-in-the-Sky/assets/112961338/21ddf961-2ba0-49b7-b36b-ea1d211d4dac)
*Soldering normally is tedious. Soldering this many times is aggravating. Soldering this many times and then being told it was unnecessary is painful.*

## `Wiring, again`
Despite the trauma of wasted time and effort, I tried to rescue this stupid PiCowbell in order to not have to solder anything ever again. The benefit of having all of these headers (which is why I intended to do this from the start) was that I could reconfigure my wiring whenever I wanted, because nothing was set in stone. This was the moment I cut the altimeter out of the plan, because it didn't fit on the board. The wiring was mostly unproblematic, I wired it all up, tested it and it output numbers as intended. The next class, I went back to it and something was wrong, because the PiCo was audibly screaming at me. **Turns out I had the battery's (+) pin on a ground rail.** A few quick adjustments and it started to work again.

# `Building A Prototype`
### `The Base`
The first part we (re)designed was the base, which was definitely the easiest part since it's designed to be built out of mostly wood.
![image](https://github.com/jvaugha3038/Pi-in-the-Sky/assets/112961338/ca71f98c-4bd6-4103-8950-3c72db984624)

The gold colored part in the middle (dubbed the "holder") is the only 3D-printed part, and the pole is metal. Everything else is wood, meaning that I didn't have to offset any of the slots that will connect them since we'll cut and sand them manually (probably), and we also likely wont need screws because the friction fits should be strong enough. The pole has space to rotate so we can turn the whole thingy without picking it up (and because Troy wanted to be able to control it like a machine gun turret, which is awesome). The side without a support will be the front, because most of the turret's weight will be in the back, which has a longer support.

### `The Block`
The Block is really simple (and probably doesn't deserve its own section), but here it is.
![image](https://github.com/jvaugha3038/Pi-in-the-Sky/assets/112961338/ddebf2f8-2ab8-48fe-889d-49d2799e297e)

This connects the top of the ballista to the pole. Not much to be said.



