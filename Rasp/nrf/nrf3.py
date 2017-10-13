import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev


class RadioNRF:

    GPIO.setmode(GPIO.BCM)

    def __init__(self, timeOut=5, trys=20):
        self.pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1],
        [0xE8, 0xE8, 0xF0, 0xF0, 0xE2]]
        self.radio = NRF24(GPIO, spidev.SpiDev())
        self.radio.begin(0, 25)
        self.radio.setPayloadSize(32)

        self.radio.setChannel(0x76)
        self.radio.setDataRate(NRF24.BR_1MBPS)
        self.radio.setPALevel(NRF24.PA_MIN)
        self.radio.setAutoAck(True)
        self.radio.enableDynamicPayloads()
        self.radio.enableAckPayload()
        self.radio.openReadingPipe(1, self.pipes[1])
        self.radio.openWritingPipe(self.pipes[0])
        self.radio.printDetails()
        self.radio.stopListening()
        self.timeOut = timeOut
        self.trys = trys

    def ForcePingPong(self):
        while True:
            receivedMessage = []
            self.radio.stopListening()
            print "Ping"
            self.radio.write("Ping")
            self.radio.startListening()
            time.sleep(1)
            if(self.radio.available(0)):
                self.radio.read(receivedMessage, 4)
                print "Rec: ", receivedMessage

    def SendTo(self, verifyByte, msg):
        for i in range(0, self.trys):  # Numero Maximo de tentativas de envio
            reciveAck = []             # Rxbuffer para o Ack
            self.radio.stopListening()
            send = '*' + verifyByte + msg
            # Byte de verificacao Fixo, e variavel
            self.radio.write(send)
            time.sleep(0.1)
            self.radio.startListening()
            for i in range(0, self.timeOut):
                if self.radio.available(0):
                    self.radio.read(reciveAck, 1)
                    print "Ack Recive: ", reciveAck[0], unichr(reciveAck[0])
                    if unichr(reciveAck[0]) == verifyByte:
                        return True
                    else:
                        print "Error: ", verifyByte, reciveAck[0]
                time.sleep(0.5)
        print "Error: retorno sem sucesso"
        return False

    def SendToKL43Z(self, ID, msg):
        self.radio.stopListening()
        for i in range(0, self.trys):
            print "Seend the ID", ID
            self.radio.write(ID)
            time.sleep(0.5)
            if self.getArk(ID) is True:
                self.radio.stopListening()
                self.radio.write(msg)
                if self.getArk(ID):
                    return True
            time.sleep(1 / 2)
        return False

    def getArk(self, ID):
        receivedMessage = []
        for i in range(0, self.timeOut):
            self.radio.startListening()
            if(self.radio.available(0)):
                self.radio.read(receivedMessage, 1)
                self.radio.stopListening()
                if(receivedMessage == ID):
                    return True
                print "ID Error !!!", receivedMessage
            time.sleep(0.50)
        print "Time OUT!"
        return False

    def ForceSendID(self, ID):
        receivedMessage = []
        while True:
            print "Send: ", ID
            self.radio.write(ID)
            time.sleep(1)
            self.radio.startListening()
            if(self.radio.available(0)):
                self.radio.read(receivedMessage, 1)
                print "ID: ", ID, "Recive: ", receivedMessage
            self.radio.stopListening()

    def ForceLiten(self):
        receivedMessage = []
        self.radio.startListening()
        while(True):
            if(self.radio.available(0)):
                self.radio.read(receivedMessage, 1)
                print "Recive: ", receivedMessage
            time.sleep(0.5)

    def exit(self):
        self.radio.end()
        GPIO.cleanup()
        print ("lean GPIO")  # Clean the GPIO

if __name__ == "__main__":
    radio = RadioNRF()
    try:
        while(radio.SendTo("B", "CRISMEAJUDA1")):
            pass
        #radio.ForceSendID("3")
    except KeyboardInterrupt:
        radio.exit()
    radio.exit()