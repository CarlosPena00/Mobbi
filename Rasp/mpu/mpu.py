import smbus
import time


class MPU:
    """ Class that get the Gyro, Acell and temperature from a MPU6050
    this module is based on:
    1) https://www.filipeflop.com/blog/tutorial-acelerometro-mpu6050-arduino/
    2) https://www.sunfounder.com/learn/sensor-kit-v2-0-for-raspberry-pi-b-plus
    3) https://github.com/Tijndagamer/mpu6050/blob/master/mpu6050/mpu6050.py
    /lesson-32-mpu6050-gyro-acceleration-sensor-sensor-kit-v2-0-for-b-plus.html
    """
    ACCEL_SCALE_MODIFIER_2G = 16384.0

    GRAVITIY_MS2 = 9.80665

    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.address = 0x68  # i2cdetect -y 1
        self.bus.write_byte_data(self.address, 0x6b, 0)  # "Wake sensor"
        # https://playground.arduino.cc/Main/MPU-6050
        self.accelConfig = 0x1C
        self.accelRang = self.bus.read_byte_data(self.address, self.accelConfig)

    def __getXYZ(self, adr):
        xyz = []
        for i in range(3):
            high = self.bus.read_byte_data(self.address, adr + i * 2)
            low = self.bus.read_byte_data(self.address, adr + i * 2 + 1)
            val = (high << 8) + low
            if (val >= 0x8000):
                val = -((65535 - val) + 1)
            xyz.append(val)
        return xyz

    def getGyro(self):
        adr = 0x43
        gyro = self.__getXYZ(adr)
        return gyro

    def getAccel(self):
        adr = 0x3B
        acell = self.__getXYZ(adr)
        acell[0] = (self.GRAVITIY_MS2 * acell[0]) / self.ACCEL_SCALE_MODIFIER_2G
        acell[1] = (self.GRAVITIY_MS2 * acell[1]) / self.ACCEL_SCALE_MODIFIER_2G
        acell[2] = (self.GRAVITIY_MS2 * acell[2]) / self.ACCEL_SCALE_MODIFIER_2G
        return acell

    def getTemp(self):
        high = self.bus.read_byte_data(self.address, 0x41)
        low = self.bus.read_byte_data(self.address, 0x42)
        val = (high << 8) + low
        if (val >= 0x8000):
            val = -((65535 - val) + 1)
        val2 = (val / 340.00) + 36.53

        return val2

mpu = MPU()

while True:
    print "Acell: ", mpu.getAccel()
    print "Temp: ", mpu.getTemp()
    time.sleep(0.5)
