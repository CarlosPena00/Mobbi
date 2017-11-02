from nrf24 import NRF24
import time

addrTx = [0xE8, 0xE8, 0xF0, 0xF0, 0xE1]
# "2Node"  # ou [ 0x32, 0x4E, 0x6F, 0x64, 0x65 ]
addrRx = [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]
#"1Node"  # ou [ 0x31, 0x4E, 0x6F, 0x64, 0x65 ]


radio = NRF24()
radio.begin(0, 0, 25, 24)
radio.openWritingPipe(addrTx)
radio.openReadingPipe(1, addrRx)
radio.startListening()
radio.printDetails()
try:
    while True:
        pipe = [0]
        if radio.available(pipe, False):
            print "Rx"
            dado = []
            radio.read(dado)
            print dado
            #radio.stopListening()
            #radio.write(dado)
            #radio.startListening()
        time.sleep(0.001)
except KeyboardInterrupt:
    print "bye"