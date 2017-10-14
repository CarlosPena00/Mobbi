import RPi.GPIO as GPIO
import time


class WeightSensor:
    """ Class that get the weight from a HX711
    this module is based on the HX711 datasheet
    """

    def __init__(self, SCK, DT, LED):
        self.SCK = SCK
        self.DT = DT
        self.LED = LED
        self.tare = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SCK, GPIO.OUT)  # SCK command
        GPIO.setup(self.DT, GPIO.IN)  # Device Output
        GPIO.setup(self.LED, GPIO.OUT)  # LED output
        GPIO.output(self.LED, False)
        #self.setTare(5)

    def __calculateWeight(self):
        while GPIO.input(self.DT) == 1:
            pass
        weight = 0
        for i in range(0, 24):
            weight = weight << 1
            GPIO.output(self.SCK, True)
            if GPIO.input(self.DT):
                weight += 1
            GPIO.output(self.SCK, False)
        GPIO.output(self.SCK, True)
        GPIO.output(self.SCK, False)
        return weight

    def setTare(self, n=3):
        count = 10000000000
        for i in range(n):
            weight = self.__calculateWeight()
            if count > weight:
                count = weight
            time.sleep(0.1)
        self.tare = count

    def getWeight(self, n=0):
        #Just read some time, not usefull at all

        for i in range(n):
            self.__calculateWeight()
        weight = self.__calculateWeight()
        if weight <= 0 or weight == 8388607 or weight >= 1660000:
            GPIO.output(self.LED, True)
            time.sleep(1)
            GPIO.output(self.LED, False)
        return (weight - self.tare), (weight - self.tare) > 60000


def autoTare(WS):
    WS.setTare(100)
    inter = 0
    negCount = 0
    lastWeight = 0
    while True:
        weight = WS.getWeight()
        if abs(lastWeight - weight) < 10000:
            inter += 1
        else:
            inter = 0
        lastWeight = weight
        print (weight)
        if weight < 0:
            negCount += 1
        if (inter == 2000 and weight < 10000) or negCount == 3:
            print("Tare")
            inter = 0
            negCount = 0
            WS.setTare(100)


if __name__ == "__main__":
    SCK_PIN = 27
    DT_PIN = 17
    LED_PIN = 22
    WS = WeightSensor(SCK_PIN, DT_PIN, LED_PIN)
    #WS.getWeight(100)
    inter = 0
    negCount = 0
    lastWeight = 0
    WS.setTare(10)
    try:
        while True:
            actualWeight = WS.getWeight(1)
            print (actualWeight)
            time.sleep(0.1)

    except KeyboardInterrupt:
        GPIO.cleanup()
        print ("lean GPIO")  # Clean the GPIO
