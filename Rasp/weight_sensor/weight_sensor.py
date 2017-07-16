import RPi.GPIO as GPIO


class WeightSensor:
    """ Class that get the weight from a HX711
    this module is based on the HX711 datasheet

    Not test yet
    """

    def __init__(self, SCK, DT):
        self.SCK = SCK
        self.DT = DT
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.SCK, GPIO.OUT)  # SCK command
        GPIO.setup(self.DT, GPIO.IN)  # Device Output

    def getWeight(self):
        weight = 0
        GPIO.output(self.SCK, False)
        while GPIO.input(self.DT):
            for i in range(0, 24):
                GPIO.output(self.SCK, True)
                weight = weight << 1
                GPIO.output(self.SCK, False)
                if GPIO.input(self.DT):
                    weight += 1
        GPIO.output(self.SCK, True)
        weight ^= 0x800000
        GPIO.output(self.SCK, False)
        return weight
