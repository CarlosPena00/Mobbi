from mpu6050 import mpu6050
import time

sensor = mpu6050(0x68)

try:
    while True:
        print "Accel: ",( sensor.get_accel_data())
        print "Gyro: ",( sensor.get_gyro_data())
        print "Temp: ",( sensor.get_temp())
        time.sleep(1)

except KeyboardInterrupt:
    print "exit"
