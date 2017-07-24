import RPi.GPIO as GPIO
from weight_sensor import WeightSensor


class Motion:

    def __init__(self):
        self.startWeight = False
        self.lastWeight = 0

    def initWeight(self, SCK_PIN, DT_PIN):
        self.WS = WeightSensor(SCK_PIN, DT_PIN)
        self.startWeight = True
        self.lastWeight = self.WS.getWeight()

    def waitUntilWeight(self):
        while True:
            try:
                self.weight = self.WS.getWeight()
                if (self.weight - self.lastWeight) > 10000:
                    return True
            except KeyboardInterrupt:
                GPIO.cleanup()
                print ("lean GPIO")  # Clean the GPIO


if __name__ == "__main__":
    SCK_PIN = 27
    DT_PIN = 17
    MT = Motion()
    MT.initWeight(SCK_PIN, DT_PIN)
    MT.waitUntilWeight()
    GPIO.cleanup()
