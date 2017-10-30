import RPi.GPIO as GPIO
import time
import Adafruit_ADS1x15
import sys
#from mpu6050 import mpu6050
#sensor = mpu6050(0x68)


class Laser:
    adc = Adafruit_ADS1x15.ADS1015()

    def __init__(self, gain):
        self.gain = gain
        print('Reading ADS1x15 values, press Ctrl-C to quit...')
        print('| {0:>6} | {1:>6} |'.format(*range(2)))
        print('-' * 37)

    def getLdr(self):
        value = [0] * 2
        for i in range(2):
            value[i] = self.adc.read_adc(i, gain=self.gain)
        b = '| {0:>6} | {1:>6} |'.format(*value)
        sys.stdout.write('\r' + b)
        sys.stdout.flush()
        time.sleep(0.05)
        #sys.stdout.write('\r' + str(sensor.get_temp()))
        #sys.stdout.flush()
        
        return b

a = Laser(1)
while 1:
    a.getLdr()
