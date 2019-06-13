import json
from pymemcache.client import base

import speech_recognition as sr 
from difflib import get_close_matches 

import time

import Adafruit_PCA9685

client = base.Client(('localhost', 11211))
shape_data_str = client.get('vision_data')

shape_data = json.loads(shape_data_str)

loca = [0,0]

print(shape_data)

sample_rate = 48000
 
chunk_size = 2048
#Initialize the recognizer 
r = sr.Recognizer() 

mic = sr.Microphone() 

color_pattern = ['blue', 'green', 'yellow', 'red']
action_pattern = ['pickup', 'drop', 'dance', 'grab']
obj_pattern = ['cube', 'square', 'cuboid', 'rectangle', 'triangle', 'prism', 'cone', 'hexagon', 'circle', 'sphere', 'ball' ]

pwm = Adafruit_PCA9685.PCA9685(address=0x42, busnum=11)

pwm.set_pwm_freq(50)


pca_addr = 0x42
min_pulse = 800
max_pulse = 2200
frequency = 60

global i
i = 90
global j
j = 30
global k
k = 90

def map_ard(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def pulseWidth(angle):
    pulse_wide = map_ard(angle, 0, 180, min_pulse, max_pulse)
    analog_value = int(float(pulse_wide) / 1000000 * frequency * 4096)
    return analog_value

pwm.set_pwm(0, 0, pulseWidth(i))
pwm.set_pwm(1, 0, pulseWidth(90))
pwm.set_pwm(2, 0, pulseWidth(90))
pwm.set_pwm(3, 0, pulseWidth(j))
pwm.set_pwm(4, 0, pulseWidth(-30))
pwm.set_pwm(5, 0, pulseWidth(0))

def closeMatches(patterns, word):
	data = word.split()
	for temp in data: 
		match_list = get_close_matches(temp, patterns)
		if len(match_list) != 0:
			return match_list[0]
	return 1

def detect():
	with mic as source: 
		#wait for a second to let the recognizer adjust the 
		#energy threshold based on the surrounding noise level 
		r.adjust_for_ambient_noise(source) 
		print("Say Something")
		#listens for the user's input 
		audio = r.listen(source) 
			
		try: 
			text = r.recognize_google(audio) 
			print("you said: " + text)
			return text 
		
		#error occurs when google could not understand what was said 
		
		except sr.UnknownValueError: 
			print("Google Speech Recognition could not understand audio")
			return 1 
		
		except sr.RequestError as e: 
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
			return -1


def not_understood():
	print("Sorry, didn't understand that!")

def run():
    if (detect() == "hey July"):
        print("what do you want?")
        instruction = detect()
        if (instruction != 1 or instruction != -1):
            action = closeMatches(action_pattern, instruction)
            if action != 1:
                print("Action: " + action)
            else:
                not_understood()
                return 0
            color = closeMatches(color_pattern, instruction)
            if color != 1:
                print("Color: " + color)
            else:
                not_understood()
                return 0
            obj = closeMatches(obj_pattern, instruction)
            if obj != 1:
                print("Object: " + obj)
                voice_dat = [action, color, obj]
                return voice_dat
            else:
                not_understood()
                return 0
        else:
            not_understood()
            return 0
    else:
        not_understood()
        return 0


while True:

    print("ACTIVE")
    voice_data = run()
    print(voice_data)
    if (voice_data != 0):
        if (voice_data[1] == "blue"):
            col = 0

        elif (voice_data[1] == "yellow"):
            col = 1

        elif (voice_data[1] == "red"):
            col = 2

        shape_data_str = client.get('vision_data')
        shape_data = json.loads(shape_data_str)
        loca[0] = shape_data[col][0][0]
        loca[1] = shape_data[col][0][1]

        # Lineup object in the X axis
        
        if(shape_data[col][0][2] == voice_data[2]):
            while ( ( ( loca[0] >= ((600/2)+10) ) or ( loca[0] <= ((600/2)-10) ) ) ):
                print("Required Object at X:" + str(loca[0]) + " Y: " + str(loca[1]))
                shape_data_str = client.get('vision_data')
                shape_data = json.loads(shape_data_str)
                loca[0] = shape_data[col][0][0]
                loca[1] = shape_data[col][0][1]
                if (loca[0] <= ((600/2)+10)):
                    if (i != 0):
                        pwm.set_pwm(0, 0, pulseWidth(i))
                        i = i - 1
                elif (loca[0] >= ((600/2)+10)):
                    if (i != 165):
                        pwm.set_pwm(0, 0, pulseWidth(i))
                        i = i + 1
                time.sleep(0.1)

            # Lineup object in the Y axis

            while ( ( ( loca[1] >= ((480/2)+10) ) or ( loca[1] <= ((480/2)-10) ) ) ):
                print("Required Object at X:" + str(loca[0]) + " Y: " + str(loca[1]))
                shape_data_str = client.get('vision_data')
                shape_data = json.loads(shape_data_str)
                loca[0] = shape_data[col][0][0]
                loca[1] = shape_data[col][0][1]
                if (loca[1] <= ((480/2)+10)):
                    if (j != 0):
                        pwm.set_pwm(3, 0, pulseWidth(j))
                        j = j - 1
                elif (loca[1] >= ((480/2)+10)):
                    if (j != 165):
                        pwm.set_pwm(3, 0, pulseWidth(j))
                        j = j + 1
                time.sleep(0.1)
            test1=0

            # Move down towards the object

            while (k <= 140):
                if (k != 160):
                    pwm.set_pwm(1, 0, pulseWidth(k))
                    pwm.set_pwm(2, 0, pulseWidth(k))
                    k = k + 1
                time.sleep(0.1)

            # Grab the object

            while (test1 != 10):
                test1 = test1 + 1
                if (j != 10):
                    pwm.set_pwm(3, 0, pulseWidth(j))
                    j = j + 1
                time.sleep(0.1)

            pwm.set_pwm(5, 0, pulseWidth(165))

            time.sleep(1)

            # Pull back the object

            while (k >= 80):
                if (k != 0):
                    pwm.set_pwm(1, 0, pulseWidth(k))
                    pwm.set_pwm(2, 0, pulseWidth(k))
                    k = k - 1

            # Reset the Arm's position

            i = 90
            j = 30
            k = 90

            pwm.set_pwm(0, 0, pulseWidth(i))
            pwm.set_pwm(1, 0, pulseWidth(90))
            pwm.set_pwm(2, 0, pulseWidth(90))
            pwm.set_pwm(3, 0, pulseWidth(j))
            pwm.set_pwm(4, 0, pulseWidth(-30))

            time.sleep(1)

            pwm.set_pwm(5, 0, pulseWidth(0))

