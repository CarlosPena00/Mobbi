import serial

ser = serial.Serial('/dev/ttyUSB0',9600)
lista = []
lista_temp = []
lista_humidade = []
count_pas = 0

while(True):
	serial_get = str(ser.readline())
	print serial_get
	if("RFID" in serial_get):
		count_pas+=1
	elif("Um_and_Temp" in serial_get):
		serial_get = serial_get.split(' ')
		# print serial_get
	else:
		serial_get = serial_get.split(' ')
		print serial_get
		# if(not(int(serial_get[1]))):
			# print "Warning"
		# else:
		lista.append(int(serial_get[0]))
	if(count_pas>10):
		print lista
		break
print lista
print count_pas
