import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.setmode(GPIO.BCM)

i = 0
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 25)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipes[1])
radio.openWritingPipe(pipes[0])
radio.printDetails()
radio.stopListening()

try:
    while True:
        radio.startListening()
        while not radio.available(0):
            time.sleep(1 / 100)

        receivedMessage = []
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        print("Received: {}".format(receivedMessage))
        print("Translating our received Message into unicode characters...")
        string = ""
        for n in receivedMessage:
            if (n >= 32 and n <= 126):
                string += chr(n)
        print("Our received message decodes to: {}".format(string))

        radio.stopListening()
        i = (i + 1) % 500
        msg = "Hello World!! - " + str(i)
        radio.write(msg)

except KeyboardInterrupt:
    radio.end()
    GPIO.cleanup()
    print ("lean GPIO")  # Clean the GPIO
