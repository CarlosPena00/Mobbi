# Lembrar:
# >>> Colocar o log_Mobbipp.txt como 'a' denovo

# GENERAL LIBS
import RPi.GPIO as GPIO
import time
import spidev

# RF LIB
from lib_nrf24 import NRF24

# LDR/LASER LIB
import Adafruit_ADS1x15

# MPU LIB
from mpu6050 import mpu6050

# COMUNICACAO SERIAL LIB
import serial

GPIO.setmode(GPIO.BCM)

ERROR_CODE_TIMEOUT_RF = 'e001'
ERROR_CODE_TIMEOUT_ESCADA = 'e002'
ERROR_CODE_LDR1 = 'e003'
ERROR_CODE_LDR2 = 'e004'
ERROR_CODE_WEIGHT = 'e005'
ERROR_CODE_QTD_ENVIOS = 'e006'
ERROR_CODE_LDR1_DC = 'e007'
ERROR_CODE_LDR2_DC = 'e008'
ERROR_CODE_WEIGHT_DC = 'e009'
TIMEOUT_NRF = 1 / 100    # 10 mili seg
TIMEOUT_ESCADA = 2    # 2 seg
TIME_SERIAL = 5    # seg
TIME_ESCADA = 0.5    # seg
VALOR_LDR = 1400
PESO = 8000
QTD_ENVIOS_MAX = 10
SCK_PIN = 27
DT_PIN = 17
LED_PIN = 22


class BUS:
    def __init__(self, ID):
        self.ID = str(ID)


class Dados:
    qtd_subiram = 0
    qtd_desceram = 0
    qtd_passagensPagas = 0
    qtd_passageirosAtual = 0
    temperatura = 0.0
    intensidadeRuido = 0
    aceleracao = []
    pckt = ""

    def __init__(self):
        self.file = open('log_Mobbipp.txt', 'w')
        datahora = str(time.strftime('%x %X')) + " - Running Mobbi++\r"
        self.file.write(datahora)

    def data_e_hora(self):
        return str(time.strftime('%x %X'))

    def criarPacote(self, ref):
        if ref == 0:
            new_aceleracao = float(sum(self.aceleracao)) / len(self.aceleracao)
            self.pckt = str(self.qtd_subiram) + "," + str(self.qtd_desceram) + "," + str(self.qtd_passagensPagas) + "," + str(self.qtd_passageirosAtual) + "," + str(self.temperatura) + "," + str(self.intensidadeRuido) + "," + str(new_aceleracao)
            return self.pckt
        else:
            return self.pckt

    def errorReport(self, errorCode):
        if errorCode == ERROR_CODE_TIMEOUT_RF:
            self.file.write(self.data_e_hora() + " - Erro: Timeout do nRF\r")
        elif errorCode == ERROR_CODE_TIMEOUT_ESCADA:
            self.file.write(self.data_e_hora() + " - Erro: Timeout dos sensores da escada\r")
        elif errorCode == ERROR_CODE_LDR1:
            self.file.write(self.data_e_hora() + " - Erro: Sensor LDR 1\r")
        elif errorCode == ERROR_CODE_LDR2:
            self.file.write(self.data_e_hora() + " - Erro: Sensor LDR 2\r")
        elif errorCode == ERROR_CODE_WEIGHT:
            self.file.write(self.data_e_hora() + " - Erro: Sensor de Peso\r")
        elif errorCode == ERROR_CODE_QTD_ENVIOS:
            self.file.write(self.data_e_hora() + " - Erro: Quantidade de envios maximo\r")
        elif errorCode == ERROR_CODE_LDR1_DC:
            self.file.write(self.data_e_hora() + " - Erro: LDR 1 desconectado\r")
        elif errorCode == ERROR_CODE_LDR2_DC:
            self.file.write(self.data_e_hora() + " - Erro: LDR 2 desconectado\r")
        elif errorCode == ERROR_CODE_WEIGHT_DC:
            self.file.write(self.data_e_hora() + " - Erro: Sensor de peso desconectado\r")


class SerialComm:
    start_time = 0
    estado = 0

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)

    def storeSerialMsg(self, dados, str_Serial):
        # Recebe uma string da forma "dado1,dado2,dado3"
        str_aux = str_Serial
        try:
            a, b, c = str_aux.split(",")
        except ValueError:
            return False
        else:
            dados.qtd_passagensPagas = int(a)
            dados.temperatura = float(b)
            dados.intensidadeRuido = int(c)
            # DEBUG
            dados.file.write('Serial read: ' + str(int(a), float(b), int(c)) + '\r')
            # /DEBUG
            return True

    def executar(self, bus, dados):
        if self.estado == 0:
            flag = self.storeSerialMsg(dados, self.ser.readline())
            self.start_time = time.time()
            self.estado = 1
        elif self.estado == 1:
            if time.time() - self.start_time > TIME_SERIAL:
                flag = self.storeSerialMsg(dados, self.ser.readline())
                self.start_time = time.time()
                if flag is False:
                    self.estado = 2
        elif self.estado == 2:
            flag = self.storeSerialMsg(dados, self.ser.readline())
            self.start_time = time.time()
            if flag is True:
                self.estado = 1


class LDR:

    def __init__(self, dados, gain=1):
        self.adc = Adafruit_ADS1x15.ADS1015()
        self.gain = gain
        if self.adc.read_adc(0, gain=self.gain) <= 100:
            dados.errorReport(ERROR_CODE_LDR1_DC)
        if self.adc.read_adc(1, gain=self.gain) <= 100:
            dados.errorReport(ERROR_CODE_LDR2_DC)

    def getLDRValue(self, ref):
        value = 0
        value = self.adc.read_adc(ref - 1, gain=self.gain)
        if value > VALOR_LDR:
            return 0
        else:
            return 1


class WeightSensor:
    """ Class that get the weight from a HX711
    this module is based on the HX711 datasheet
    """

    def __init__(self, SCK, DT, LED, dados):
        self.SCK = SCK
        self.DT = DT
        self.LED = LED
        self.tare = 0
        GPIO.setup(self.SCK, GPIO.OUT)  # SCK command
        GPIO.setup(self.DT, GPIO.IN)  # Device Output
        GPIO.setup(self.LED, GPIO.OUT)  # LED output
        GPIO.output(self.LED, False)
        if self.getWeight() == 8388607 or self.getWeight() == 1660000:
            dados.errorReport(ERROR_CODE_WEIGHT_DC)
        self.setTare(10)

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
        return (weight - self.tare)


class NRF:
    pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]
    start_time = 0
    qtd_envios = 0
    estado = 0

    def __init__(self, csn, ce):
        self.radio = NRF24(GPIO, spidev.SpiDev())
        self.radio.begin(csn, ce)
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
        self.radio.stopListening()

    def receive_msg(self):
        self.radio.startListening()
        receivedMessage = []
        self.radio.read(receivedMessage, self.radio.getDynamicPayloadSize())
        string = ""
        for n in receivedMessage:
            if (n >= 32 and n <= 126):
                string += chr(n)
        return string

    def send_msg(self, msg):
        self.radio.stopListening()
        self.radio.write(msg)
        self.radio.startListening()

    def executar(self, bus, dados):
        # ENVIA ID
        if self.estado == 0:
            msg = str(time.strftime('%x_%X,')) + bus.ID
            self.send_msg(msg)
            self.start_time = time.time()
            self.estado = 1

        # RECEBE ACK DO ID
        elif self.estado == 1:
            rcvd_msg = self.receive_msg()

            if (time.time() - self.start_time >= TIMEOUT_NRF):
                dados.errorReport(ERROR_CODE_TIMEOUT_RF)
                self.estado = 0
            elif rcvd_msg == bus.ID + "_ID_ACK":
                self.qtd_envios = 0
                self.estado = 2

        # ENVIA DADOS
        elif self.estado == 2:
            self.send_msg(dados.criarPacote(self.qtd_envios))
            self.qtd_envios += 1
            self.start_time = time.time()
            self.estado = 3

        # RECEBE ACK DOS DADOS
        elif self.estado == 3:
            rcvd_msg = self.receive_msg()

            if (time.time() - self.start_time >= TIMEOUT_NRF and self.qtd_envios < QTD_ENVIOS_MAX):
                dados.errorReport(ERROR_CODE_TIMEOUT_RF)
                self.estado = 2
            elif rcvd_msg == bus.ID + "_DATA_ACK":
                dados.file.write(dados.data_e_hora() + " - Pacote enviado\r" + dados.pckt + "\r")
                self.qtd_envios = 0
                self.estado = 0
            elif rcvd_msg == bus.ID + "_DATA_NACK":
                self.qtd_envios = 0
                self.estado = 2
            elif self.qtd_envios >= QTD_ENVIOS_MAX:
                dados.errorReport(ERROR_CODE_QTD_ENVIOS)
                self.qtd_envios = 0
                self.estado = 0


class Sensors:
    count = 0
    estado = 0
    start_time = 0

    def __init__(self, dados):
        self.ldr = LDR(dados)
        self.peso = WeightSensor(SCK_PIN, DT_PIN, LED_PIN, dados)
        self.mpu = mpu6050(0x68)

    def barreira1(self, dados):
        # SWITCH (ESTADO)
        # CASE 0
        if self.estado == 0:
            # DEBUG
            dados.file.write("Entrou barreira1 - estado 0\r")
            # /DEBUG
            if self.ldr.getLDRValue(1) == 1:
                self.start_time = time.time()
                self.estado = 1
                return 1
            return 0
        # CASE 1
        elif self.estado == 1:
            # DEBUG
            dados.file.write("Entrou barreira1 - estado 1\r")
            # /DEBUG
            if self.peso.getWeight() > PESO:    # COLOCAR A CONDICAO CERTA
                self.estado = 2
            elif self.ldr.getLDRValue(2) == 1:
                dados.errorReport(ERROR_CODE_WEIGHT)
                self.estado = 0
            elif time.time() - self.start_time > TIMEOUT_ESCADA:
                dados.errorReport(ERROR_CODE_TIMEOUT_ESCADA)
                self.estado = 0
            return 1
        # CASE 2
        elif self.estado == 2:
            # DEBUG
            dados.file.write("Entrou barreira1 - estado 2\r")
            # /DEBUG
            if self.ldr.getLDRValue(2) == 1:
                dados.qtd_subiram += 1
                # DEBUG
                dados.file.write("Subida de passageiros\r")
                print ("Subida de passageiros")
                # /DEBUG
                self.estado = 0
                return 0
            elif time.time() - self.start_time > TIMEOUT_ESCADA:
                dados.errorReport(ERROR_CODE_LDR2)
                self.estado = 0
                return 0
            return 1

    def barreira2(self, dados):
        # SWITCH (ESTADO)
        # CASE 0
        if self.estado == 0:
            # DEBUG
            dados.file.write("Entrou barreira2 - estado 0\r")
            # /DEBUG
            if self.ldr.getLDRValue(2) == 1:
                self.start_time = time.time()
                self.estado = 1
                return 2
            return 0
        # CASE 1
        elif self.estado == 1:
            # DEBUG
            dados.file.write("Entrou barreira2 - estado 1\r")
            # /DEBUG
            if self.ldr.getLDRValue(1) == 1:
                self.estado = 2
            elif self.peso.getWeight() > PESO:    # COLOCAR A CONDICAO CERTA
                dados.errorReport(ERROR_CODE_LDR1)
                self.estado = 0
            elif time.time() - self.start_time > TIMEOUT_ESCADA:
                dados.errorReport(ERROR_CODE_TIMEOUT_ESCADA)
                self.estado = 0
            return 2
        # CASE 2
        elif self.estado == 2:
            # DEBUG
            dados.file.write("Entrou barreira2 - estado 2\r")
            # /DEBUG
            if self.peso.getWeight() > PESO:    # COLOCAR A CONDICAO CERTA
                dados.qtd_desceram += 1
                # DEBUG
                dados.file.write("Descida de passageiros\r")
                print ("Descida de passageiros")
                # /DEBUG
                self.estado = 0
                return 0
            elif time.time() - self.start_time > TIMEOUT_ESCADA:
                dados.errorReport(ERROR_CODE_WEIGHT)
                self.estado = 0
                return 0
            return 2

    def degrau(self, dados):
        # SWITCH ESTADO
        # CASE 0
        if self.estado == 0:
            # DEBUG
            dados.file.write("Entrou Degrau    - estado 0\r")
            # /DEBUG
            teste = self.peso.getWeight()
            print teste
            if teste > PESO:    # COLOCAR A CONDICAO CERTA
                self.start_time = time.time()
                self.estado = 1
                return 3
            return 0
        # CASE 1
        elif self.estado == 1:
            # DEBUG
            dados.file.write("Entrou Degrau    - estado 1\r")
            # /DEBUG
            teste = self.peso.getWeight()
            print teste
            if teste < PESO:
                self.estado = 2
            elif time.time() - self.start_time > TIMEOUT_ESCADA:
                dados.errorReport(ERROR_CODE_TIMEOUT_ESCADA)
                self.estado = 0
            return 3
        # CASE 2
        elif self.estado == 2:
            # DEBUG
            dados.file.write("Entrou Degrau    - estado 2\r")
            # /DEBUG
            if self.ldr.getLDRValue(1) == 1:
                self.estado = 3
#            elif self.ldr.getLDRValue(2) == 1:
#                dados.errorReport(ERROR_CODE_LDR1)
#                self.estado = 0
            elif time.time() - self.start_time > TIMEOUT_ESCADA:
                dados.errorReport(ERROR_CODE_TIMEOUT_ESCADA)
                self.estado = 0
            return 3
        # CASE 3
        elif self.estado == 3:
            # DEBUG
            dados.file.write("Entrou Degrau    - estado 3\r")
            # /DEBUG
            if self.ldr.getLDRValue(2) == 1:
                dados.qtd_subiram += 1
                # DEBUG
                dados.file.write("Subida de passageiros\r")
                print ("Subida de passageiros")
                # /DEBUG
                self.start_time = time.time()
                self.estado = 4
                return 3
            elif time.time() - self.start_time > TIMEOUT_ESCADA:
                dados.errorReport(ERROR_CODE_WEIGHT)
                self.estado = 0
                return 0
            return 3
        # CASE 4
        elif self.estado == 4:
            # DEBUG
            dados.file.write("Entrou Degrau    - estado 4\r")
            # /DEBUG
            if time.time() - self.start_time > TIME_ESCADA:
                self.estado = 0
                return 0
            return 3

    def mpu_func(self, dados):
        valor = self.mpu.get_accel_data()
        maior = max(valor)
        dados.aceleracao.append(maior)

    def executar(self, bus, dados):
        if self.count == 0:
            self.mpu_func(dados)
            # self.count = self.barreira1(dados)
            if self.count == 0:
                self.count = self.barreira2(dados)
            if self.count == 0:
                self.count = self.degrau(dados)
        elif self.count == 1:
            self.mpu_func(dados)
            self.count = self.barreira1(dados)
        elif self.count == 2:
            self.mpu_func(dados)
            self.count = self.barreira2(dados)
        elif self.count == 3:
            self.mpu_func(dados)
            self.count = self.degrau(dados)
