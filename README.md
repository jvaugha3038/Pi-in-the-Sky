# Pi-in-the-Sky

&nbsp;

# `Table of Contents`
* [Goal](#goal)
* [Planning](#planning)
* [Coding](#coding)
* [Wiring](#wiring)
* [The Design](#the_design)
* [Building](#building)
* [Launch and Data](#launch_and_data)
* [Problems](#problems)
* [Reflection](#reflection)

&nbsp;
# `Goal`
The goal of the project was to get the Pico into the air, somehow, and then collect useful data that can be retrieved. We chose to do so by launching it out of a ballista-style turret. We used a gyroscope/accelerometer to record the payload's current angle, and it's angular acceleration.

# `Planning`
[Link to planning Document](https://docs.google.com/document/d/14-PHrZZvjooZSPuYYvAT_kGfdMwqDnR2ftNQUhQHIGQ/edit)

The plans changed quite frequently, as we found some designs better than others, or decided to scrap some ideas entirely, but I'll get into that in relevant sections.

# `Coding`
The main idea for our design was partially based on the fact that neither of us excelled at code nor wanted to be the one to write it all, so we made sure the code was almost entirely comprised of things we knew how to do. By that I mean that the project code is essentially an altered version of my code for a previous assignment. I'll go through it in chunks.

```python
#type:ignore

import adafruit_mpu6050
import busio
import time
import board
from digitalio import DigitalInOut, Direction #import soup

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT #setting up onboard led
purp = DigitalInOut(board.GP16)
purp.direction = Direction.OUTPUT #setting up tilt light

sda_pin = board.GP14
scl_pin = board.GP15
i2c = busio.I2C(scl_pin, sda_pin)
mpu = adafruit_mpu6050.MPU6050(i2c, address=0x68) #setting up the i2c device (gyro/accelerometer)

prev=0
deg=0
s=0.2 #set time to wait between data saves
#the setup soup is now over
```
All of this is just the imports and Pico pin setup, aptly titled "the setup soup". I'll only refer to it as such from now on. The "#type:ignore" is just so it doesn't spit out problems that don't actually exist, because otherwise it complains about every single import despite it all working fine.

```python
def data(s): #function that grabs data
    global prev
    global deg
    global acc
```
The data processing is in a function separate from the data saving loop, in order to speed up the code and make it easier to read. These global variables exist so the code remembers to grab these numbers instead of the irrelevant ones defined outside of the function.

```python
    prev = deg
    deg=(round(float(mpu.gyro[0] + 0.08), 1)*(s)*(180/3.14159))+prev #converting radians/second into just degrees
```
These two lines caused a lot of pain. The idea is that every time the code runs through the loop, it sets the previous degrees variable to what the degrees variable was the last time, to store it. The new angle, which would be the difference between the current angle and the previous angle, is then calculated and added to the previous one. This SHOULD create an accurate way to keep track of the angle. However, since the gyroscope measures angle in radians per second, we have to convert it to static degrees. Thats what the 180/pi, and the 0.2 (the time it SHOULD take to loop once) are for. As evidenced by my use of the word SHOULD, it did not do this. Despite having done this exact code in a project from last year (i even copied the code), it just didn't work, so I benched the code for a bit to work on other things. Turns out that the problem was that the gyroscope had to be calibrated, which is what that 0.08 is for. When it's flat on the table, it reads something close to -0.08 rad/s, so that offset negates it, and then it's all rounded so the angle is correctly said to not be changing when the device isn't moving.

I also wanted to keep track of the height the payload was at, but the altimeter caused a lot of wiring and code pain and output horribly inconsistent numbers (which would require knowing the sea level at all times to be fully accurate), so I scrapped it to save my sanity.

```python
    acc = mpu.acceleration
    print("X = ["+str(acc[0])+"]| Y = ["+str(acc[1])+"]| Z = ["+str(acc[2])+"]| ANGLE = ["+str(deg)+"]")
    #prints acceleration values using the archaic str() method
    if acc[2] <= 0:
        purp.value = True #if number small light go
        tilt=1
    else:
        purp.value = False #if number big light no
        tilt=0
```
The first line just shortens the sensor name into a tiny variable for readability. The second line prints out all of the sensor variables for testing. The lines below simply light up an LED when its tilted sideways, which is a remnant of my older code that this is based on. I considered removing the LED and keeping just the variable itself, until I noticed that it was purple and I think its cool enough to keep.

```python
with open("/data.csv", "a") as datalog: #the thing that allows the data to be Grabbed
    while True: #the Loop
```
These two lines open up an excel sheet named data.csv, which is where all of the outputs will go, and also set up The Loop, which is the rest of the code.

```python
        tilt, deg = data(s) #calls function and gets variables
        t=time.monotonic()
        datalog.write(f"{t},{acc[0]},{acc[1]},{acc[2]},{tilt},{deg}\n") #the format of each line in the data table, using the better f string method
        led.value = True #blink when data is saved
        time.sleep(0.2) #wait
        datalog.flush()
        led.value = False 
```
The final chunk starts with calling the data function and another shorthand variable, both of which I've already talked about. The second line is the line that takes all of the important output variables and copies them into the excel sheet from earlier. Then, it blinks the Pico's onboard LED for a specific amount of time, and then the loop repeats.

The final code file itself may end up looking different from this breakdown (more polished, probably,) but this is how the code works, regardless of how it looks later.

# `Wiring`
![image](https://github.com/jvaugha3038/Pi-in-the-Sky/assets/112961338/05e19ca0-2158-42b5-8595-c7d7772389b9)
*Wiring as seen on a breadboard. Neat and tidy.*

The initial wiring consisted of an LED, a switch, the battery, the gyroscope/accelerometer, and the altimeter. Then I cut the altimeter out for numerous reasons, one of them being that trying to wire all of this together on the far-too-small PiCowbell would have been awful, which is what we had to use. Despite my precautions, I still lost my mind. 

## `Soldering`
This subsection exists because I made one fatal error that would then waste almost two weeks of time: daring to be one of the first people in the class to solder headers onto the PiCowbell, instead of waiting for someone else to do it correctly and learning off of them. The PiCowbell is essentially a more compact and practical prototype shield, but it required soldering wires onto it as opposed to using jumper wires. My mistake was soldering headers onto nearly every pin in the workspace in the middle of the board, which, plus the power and ground sections as well as the ~40 headers that would connect the Pico to the PiCowbell, led to over 100 pins to solder and hours of sadness. Most of it was mindless busywork until I was then told that I didn't need to do all of that, because I could've just soldered wires straight onto the board.
![pain](https://github.com/jvaugha3038/Pi-in-the-Sky/assets/112961338/21ddf961-2ba0-49b7-b36b-ea1d211d4dac)
*Soldering normally is tedious. Soldering this many times is aggravating. Soldering this many times and then being told it was unnecessary is painful.*

## `Wiring, again`
![20240425_134130](https://github.com/jvaugha3038/Pi-in-the-Sky/assets/112961338/846c699a-84d4-4d0a-88e9-3b634214e4bb)
*Wiring as seen on the PiCowbell. Not neat or tidy.*

Despite the trauma of wasted time and effort, I tried to rescue this stupid PiCowbell in order to not have to solder anything ever again. The benefit of having all of these headers (which is why I intended to do this from the start, and continued post-dream-crushing) was that I could reconfigure my wiring whenever I wanted, because nothing was set in stone. This was the moment I cut the altimeter out of the plan, because it didn't fit on the board. The wiring was mostly unproblematic despite looking quite problematic. I wired it all up, tested it and it output numbers as intended. The next class, I went back to it and something was wrong, because the PiCo was audibly screaming at me. **Turns out I had the battery's (Switch) pin on a ground rail.** A few quick adjustments and it started to work again.

The LED in this picture wasn't soldered by me, but the fact that its purple made up for how ugly it is. This picture was taken before the payload was printed, which is when I made the switch and LED better so they could fit into it.

# `The Design`
### `The Base`
The first part we (re)designed was the base, which was definitely the easiest part since it's designed to be built out of mostly wood.

![image-removebg-preview](https://github.com/jvaugha3038/Pi-in-the-Sky/assets/112961338/70f99c92-d6f8-49c7-b646-60bfcd11c10b)

The gold colored part in the middle (dubbed the "holder") is the only 3D-printed part, and the pole is a PVC pipe. Everything else is wood, meaning that I didn't have to offset any of the slots that will connect them since we'll cut and sand them manually (probably), and we also likely wont need screws because the friction fits should be strong enough. The pole has space to rotate so we can turn the whole thingy without picking it up (and because Troy wanted to be able to control it like a machine gun turret, which is both awesome and not allowed), but despite that, we opted to screw the supports straight through the holder and into the pipe so it can't turn. The side without a support will be the front, because most of the turret's weight will be in the back, which has a longer support.

### `The Block`
The Block is really simple (and probably doesn't deserve its own section), but here it is.

![image-removebg-preview (1)](https://github.com/jvaugha3038/Pi-in-the-Sky/assets/112961338/98aa8b58-e8c3-47a2-9b38-378f5a312c6e)

This connects the top of the ballista to the pole. Not much to be said.

### `The Top`
This is the main part of the ballista, but since most of this is wood (the walls and base), I'll instead focus on the crank part.

![image-removebg-preview (2)](https://github.com/jvaugha3038/Pi-in-the-Sky/assets/112961338/23ee0226-5aa1-4017-922d-45283397e355)

*turret, with walls*

![image-removebg-preview (3)](https://github.com/jvaugha3038/Pi-in-the-Sky/assets/112961338/603d9345-00cd-4175-8d62-db72ce1e2c6c)

*turret, without walls*

Ignoring the grey handle, which is a remnant of Troy wanting to be able to control it like a turret (which we are, again, not allowed to do), this is the crank part. The orange handle can be turned to rotate the light grey pole in the middle, which will have a string connected to it. This will pull back a board that has the projectile on the other end, and when the crank is released, the board will get pulled forward again by some rubber stretch bands. Said board isn't in the Onshape document because the idea is we design it with the payload in mind.

### `The Payload`
This thing holds the Pico and all of its wires nice and compact, so it doesn't explode on impact and so the wires (hopefully) don't get disconnected.

![image-removebg-preview (4)](https://github.com/jvaugha3038/Pi-in-the-Sky/assets/112961338/8616b7dc-2e93-4ddf-91b1-6ddae7320737)

The holes on the side hold the LED and the switch, and the Pico is screwed into the bottom with the pins up so the PiCowbell can be connected. The little divit on the side is designed to perfectly fit the battery, and the holes above it are so the mpu6050 (gyroscope) can be secured with screws. That part didn't work, because the holes aren't perfectly aligned, but that's fine. Basically, this thing is gonna be surrounded in styrofoam, and we're gonna launch a styrofoam block.

![20240503_133534](https://github.com/jvaugha3038/Pi-in-the-Sky/assets/112961338/d32a1662-6255-4ee2-87d7-692430a14973)
![20240503_133459](https://github.com/jvaugha3038/Pi-in-the-Sky/assets/112961338/5755f30f-5ba4-4221-83ae-1c3b8d244fb4)
*This was a complete nightmare to design since I couldnt find an onshape model for the picowbell or mpu6050 in the CHS folder. It was so worth it though. This thing looks sick. You can barely even SEE the battery in there.*

# `Building`

# `Launch and Data`

# `Problems`
### `Big Problems`
* The altimeter, and all of the pain it wanted to cause.
    * Simply choose to not use an altimeter anymore.
* The part connecting the top to the base of the ballista had two joints.

  ![image](https://github.com/jvaugha3038/Pi-in-the-Sky/assets/112961338/fe1dfd6b-490c-4936-bbf4-7373ff164127)

    * This was the first real design for the "block" part, in which it was actually two parts. Those mostly transparent pieces would have holes in them, so you could push a rod or something through it and into one of the 5 holes on the grey block (making the sketch of the grey part successfully mirror itself to the other side was half of the battle, but thats irrelevant). I noticed this horrible and redundant design flaw after designing it, and then immediately sought to fix it. I created a better design that removed those see-through parts and essentially combined them with the blue part. However, connecting the grey part to that was not a problem I wanted to bother solving, so I scrapped that one too and made the current block design: a blue block that just doesn't rotate at all.
* [Soldering.](#soldering)
* Github didn't want to connect to VSCode.
    * I don't even know what was going on. I heard it was something to do with Securly blocking some part of Github that likely didn't need to be blocked at all (thanks CHS). I just gave up and downloaded the file and put it here, so I can't actually push changes to github without doing that again.
* TIME.
    * So many time-based problems. Troy is a senior, so he leaves in late May, essentially meaning we're done for if we don't at least launch it once before then. Both of us were part of this out-of-school engineering ethics collaboration between us, UVA, and Hampton university, so we missed 2 days for that. We are in completely different AP exams, so we're rarely able to work together in May. If this thing breaks before the launch we are completely ruined, because rebuilding this wooden turret is just simply not going to happen.

### `Smaller Problems`
* Using the heat gun and heat-shrink wrap.
    * This one is a skill issue. I apparently don't know what I'm doing. The only reason it's there is because I didn't like the exposed metal on the LED wires, which it does technically cover, but it can slide up and down on the wire which is probably not good.
  
# `Reflection`
