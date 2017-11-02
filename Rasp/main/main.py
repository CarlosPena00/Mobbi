from LIB import *

# SETUP
bus = BUS("0791")    # ID do onibus
dados = Dados()
sensors = Sensors(dados)
serial = SerialComm()
rf = NRF(0, 25)
arq = open('time_Mobbipp.txt', 'w')
arq.write(dados.data_e_hora() + '\r')

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

        rf.executar(bus, dados)

# EXCEPT
except KeyboardInterrupt:
        GPIO.cleanup()
        arq.close()
        print ("lean GPIO")  # Clean the GPIO
