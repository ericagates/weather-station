#!/usr/bin/env python
#
# GrovePi Example for using the Grove Temperature & Humidity Sensor Pro 
# (http://www.seeedstudio.com/wiki/Grove_-_Temperature_and_Humidity_Sensor_Pro)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  
# You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''

#ERICA GATES CS-350 FINAL PROJECT


## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
import grovepi
import math
import time #added to slow readings
from grove_rgb_lcd import *  #added to use the grove lcd rgb as a display
import json #added to use json database file for storing output
import sys

# Connect the Grove Temperature & Humidity Sensor Pro to digital port D8
# This example uses the blue colored sensor.
# SIG,NC,VCC,GND
sensor = 8  # The Sensor goes on digital port 8.

# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 0

# Connect the blue LED to digital port D2
# SIG,NC,VCC,GND
blueLed = 2

# Connect the LED to digital port D3
# SIG,NC,VCC,GND
greenLed = 3  

# Connect the red LED to digital port D4
# SIG,NC,VCC,GND
redLed = 4   

# Turn on weather system once sensor exceeds threshold resistance (daytime)
threshold = 10

grovepi.pinMode(light_sensor,"INPUT")
grovepi.pinMode(blueLed,"OUTPUT")
grovepi.pinMode(greenLed,"OUTPUT")
grovepi.pinMode(redLed,"OUTPUT")

# temp_humidity_sensor_type
# Grove Base Kit comes with the blue sensor.
blue = 0    # The Blue colored sensor.
white = 1   # The White colored sensor.

#sets LCD backlight color to purple
setRGB(255, 0, 255)

#to prepare to ouptut the weather in a JSON database file
#first create and empty dict and create a key
output = {}
output['weather'] = []


while True:
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(light_sensor)

        # Calculate resistance of sensor in K
        # I received an divide by zero error so I am adding an
        # if statement to account for whent the sensor_value is 0        
        if sensor_value <= 0:
            resistance = 0
        else:
            resistance = (float)(1023 - sensor_value) * 10 / sensor_value

        # if the resistance is lower than the threshold the sensor value is high (meaning more light)
        # we want to record temperature and humidity during light conditions only
        if resistance <= threshold:
   
        
            # This example uses the blue colored sensor. 
            # The first parameter is the port, the second parameter is the type of sensor.
            [temp,humidity] = grovepi.dht(sensor,blue)

            #check if there are nan (not a number)
            #if no nan errors, proceed
            if math.isnan(temp) == False and math.isnan(humidity) == False:
                
                f = (temp*9/5)+32 #covert temperature to farenheit

                print("temp = %.02f F humidity =%.02f%%"%(f, humidity)) #output 
                
                #code for LCD RGB Backlight Display
                t = str(f) #store temperature as a string in variable t 
                h = str(humidity) #store humidity as a string in variable h
        
      
                setText("Temp:" + t + "F\nHumidity: " + h + "%") #call function to display to LCD
                
     
                if (60.0 < f < 85.0) and (humidity < 80.0):
                    # Send HIGH to switch on green LED
                    grovepi.digitalWrite(greenLed,1)
                
                if (85.0 <= f < 95.0) and (humidity < 80.0):
                    # Send HIGH to switch on blue LED
                    grovepi.digitalWrite(blueLed,1)

                if (f >= 95.0):
                    # Send HIGH to switch on blue LED
                    grovepi.digitalWrite(redLed,1)
                
                if (humidity >= 80.0):
                    # Send HIGH to switch on blue LED
                    grovepi.digitalWrite(blueLed,1)
                    grovepi.digitalWrite(greenLed,1)
               
                            
                
                # add weater information to the output dict
                output['weather'].append({'Temp': t, 'Humidity': h})
                
                #creates a file called outputData and opens it in write code, respresented as variable 'file'
                with open ('outputData.json', 'w') as file:
                    json.dump(output, file, indent  = 2)
                
                #wait 30 minutes before updating 
                secondsPerMinute = 60.0
                minutes = 30.0
                waitTime =  minutes * secondsPerMinute
                time.sleep(waitTime)
                #reset LEDs before next reading
                grovepi.digitalWrite(blueLed,0)
                grovepi.digitalWrite(greenLed,0)
                grovepi.digitalWrite(redLed,0)
                
                
                
            
            else: #if there is nan
                #raise a type error exception
                raise TypeError('nan error')
        
        # if the resistance is higher than the threshold, the sensor value is low (low/no light)
        # turn of LEDs and wait wait for daylight, we want to record temperature and humidity during light conditions only
        else:
            # Send LOW to switch off LEDs
            grovepi.digitalWrite(blueLed,0)
            grovepi.digitalWrite(greenLed,0)
            grovepi.digitalWrite(redLed,0)
            # reset LCD with waiting message no color
            setText("waiting for daylight")
            setRGB(0,0,0)
            time.sleep(3.0)
            
    

#this exception handling code was derived from GrovePi's Github page
#Home Weather Display Project example at:
#https://github.com/DexterInd/GrovePi/blob/master/Projects/Home_Weather_Display/Home_Weather_Display.py
    except (IOError, TypeError) as e:
        print(str(e))
        # and since we got a type error
        # then reset the LCD's text and color
        setText("")
        setRGB(0,0,0)
        grovepi.digitalWrite(blueLed,0)
        grovepi.digitalWrite(greenLed,0)
        grovepi.digitalWrite(redLed,0)

    except KeyboardInterrupt as e:
        print(str(e))
        # since we're exiting the program
        # reset LCD with a blank text and no color
        setText("")
        setRGB(0,0,0)
        grovepi.digitalWrite(blueLed,0)
        grovepi.digitalWrite(greenLed,0)
        grovepi.digitalWrite(redLed,0)
        break


    
sys.exit()
