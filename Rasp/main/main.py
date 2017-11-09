from LIB import *

# SETUP
bus = BUS("0791")    # ID do onibus
dados = Dados()
sensors = Sensors(dados)
serial = SerialComm()
# rf = NRF(0, 25)
arq = open('time_Mobbipp.txt', 'w')
arq.write(dados.data_e_hora() + '\r')

# DEBUG
# i = 0
# /DEBUG

# LOOP
try:
    while (True):
        arq.write("****************\r")

        tempo = time.time()
        sensors.executar(bus, dados)
        arq.write('sensores:' + str(time.time() - tempo) + '\r')

        tempo = time.time()
        serial.executar(bus, dados)
        arq.write('serial:  ' + str(time.time() - tempo) + '\r')

        # tempo = time.time()
        # rf.executar(bus, dados)
        # arq.write('serial:  ' + str(time.time() - tempo) + '\r')

# DEBUG
        # i += 1
        # if i % 15 == 0:
        dados.printInfo()
# /DEBUG

# EXCEPT
except KeyboardInterrupt:
        GPIO.cleanup()
        arq.close()
        print ("lean GPIO")  # Clean the GPIO
