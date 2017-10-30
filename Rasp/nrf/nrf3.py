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

        self.radio.setChannel(0x74)
        self.radio.setDataRate(NRF24.BR_1MBPS)
        self.radio.setPALevel(NRF24.PA_MAX)
        self.radio.setAutoAck(True)
        self.radio.enableDynamicPayloads()
        self.radio.enableAckPayload()
        self.radio.openReadingPipe(1, self.pipes[1])
        self.radio.openWritingPipe(self.pipes[0])
        self.radio.printDetails()
        print ""
        print ""
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

    def toHex(self, num):
        var = hex(num).replace("0x", "")
        if len(var) is 1:
            var = '00' + var
        if len(var) is 2:
            var = '0' + var
        if len(var) > 3:
            print "Size bigger than 2 bytes, var set to zero"
            var = '000'
        print "Number:", num, "Hex", var
        return var

    def createPackage(self, ID, quant, temp, sound, vel):
        print "Create Package with"
        print "ID:", ID, "Number of People", quant
        print "Temperature", temp, "Sound Warnings", sound,
        print "Speed Warnings", vel
        print ""

        package = ''
        package += self.toHex(ID)
        package += self.toHex(quant)
        package += self.toHex(temp)
        package += self.toHex(sound)
        package += self.toHex(vel)
        self.radio.stopListening()
        return package

    def sendTo(self, verifyByte, msg):
        send = '*' + verifyByte + msg
        print ''
        print send, "Msg size:", len(send)
        print ''

        for i in range(0, self.trys):  # Numero Maximo de tentativas de envio
            reciveAck = []             # Rxbuffer para o Ack
            self.radio.stopListening()
            # Byte de verificacao Fixo, e variavel
            time.sleep(0.5)
            self.radio.write(send)
            self.radio.startListening()
            for i in range(0, self.timeOut):
                if self.radio.available(0):
                    self.radio.read(reciveAck, 1)
                    print "Ack Recive: ", reciveAck[0], unichr(reciveAck[0])
                    if unichr(reciveAck[0]) == verifyByte:
                        return True
                    else:
                        print "Error: ", verifyByte, reciveAck[0]
                time.sleep(0.2)
        print "Error: retorno sem sucesso"
        return False

    def exit(self):
        self.radio.end()
        GPIO.cleanup()
        print ("Clean GPIO")  # Clean the GPIO

if __name__ == "__main__":
    radio = RadioNRF()
    msg = radio.createPackage(149, 41, 29, 4, 1)
    radio.sendTo('B', msg)
    radio.exit()

#
#    try:
#        while(radio.SendTo("B", "CRISMEAJUDA1")):
#            pass
#        #radio.ForceSendID("3")
#    except KeyboardInterrupt:
#        radio.exit()
#    radio.exit()
