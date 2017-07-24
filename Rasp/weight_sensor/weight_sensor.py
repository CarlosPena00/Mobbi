import RPi.GPIO as GPIO
import time


class WeightSensor:
    """ Class that get the weight from a HX711
    this module is based on the HX711 datasheet
    """

    def __init__(self, SCK, DT):
        self.SCK = SCK
        self.DT = DT
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SCK, GPIO.OUT)  # SCK command
        GPIO.setup(self.DT, GPIO.IN)  # Device Output

    def getWeight(self):
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


if __name__ == "__main__":
    SCK_PIN = 26
    DT_PIN = 20
    WS = WeightSensor(SCK_PIN, DT_PIN)
    try:
        while True:
            print (WS.getWeight())
            time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print ("lean GPIO")  # Clean the GPIO


