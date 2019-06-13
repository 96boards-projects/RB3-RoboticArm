from __future__ import division
from pymemcache.client import base
import time
import Adafruit_PCA9685

client = base.Client(('localhost', 11211))
a = client.get('arm_tx')

pwm = Adafruit_PCA9685.PCA9685(address=0x42, busnum=11)

pwm.set_pwm_freq(50)


pca_addr = 0x42
min_pulse = 800
max_pulse = 2200
frequency = 60

i = 90
j = 30
k = 90


def map_ard(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def pulseWidth(angle):
    pulse_wide = map_ard(angle, 0, 180, min_pulse, max_pulse)
    analog_value = int(float(pulse_wide) / 1000000 * frequency * 4096)
    return analog_value

def main():

    pwm.set_pwm(0, 0, pulseWidth(i))
    pwm.set_pwm(1, 0, pulseWidth(90))
    pwm.set_pwm(2, 0, pulseWidth(90))
    pwm.set_pwm(3, 0, pulseWidth(j))
    pwm.set_pwm(4, 0, pulseWidth(-30))
    pwm.set_pwm(5, 0, pulseWidth(0))

    while True:
        a = client.get('arm_tx')
        if (a == 'a' and i != 165):
            pwm.set_pwm(0, 0, pulseWidth(i))
            i = i + 1

        elif (a == 'd' and i != 0):
            pwm.set_pwm(0, 0, pulseWidth(i))
            i = i - 1

        elif (a == 'w' and j != 165):
            pwm.set_pwm(3, 0, pulseWidth(j))
            j = j + 1

        elif (a == 's' and j != 0):
            pwm.set_pwm(3, 0, pulseWidth(j))
            j = j - 1

        elif (a == 'r' and k != 160):
            pwm.set_pwm(1, 0, pulseWidth(k))
            pwm.set_pwm(2, 0, pulseWidth(k))
            k = k + 1
            if ( k >= 159 ):
                a = 's'
                client.set('arm_tx', a)

        elif (a == 'f' and k != 0):
            pwm.set_pwm(1, 0, pulseWidth(k))
            pwm.set_pwm(2, 0, pulseWidth(k))
            k = k - 1
            if ( k <= 80 ):
                a = 'q'
                client.set('arm_tx', a)

        elif (a == 'c'):
            pwm.set_pwm(5, 0, pulseWidth(165))

        elif (a == 'o'):
            pwm.set_pwm(5, 0, pulseWidth(0))

        elif (a == 'm'):
            pwm.set_pwm(0, 0, pulseWidth(i))
            pwm.set_pwm(1, 0, pulseWidth(90))
            pwm.set_pwm(2, 0, pulseWidth(90))
            pwm.set_pwm(3, 0, pulseWidth(j))
            pwm.set_pwm(4, 0, pulseWidth(-30))
            pwm.set_pwm(5, 0, pulseWidth(0))
            i = 90
            j = 30
            k = 90

        a = 'k'
        client.set('arm_tx', a)

main()