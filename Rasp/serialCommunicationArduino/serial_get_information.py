import serial

ser = serial.Serial('/dev/ttyACM0',9600)
lista = []
count_pas = 0

while(True):
	serial_get = str(ser.readline())
	print serial_get
	if(len(serial_get)>7):
		count_pas+=1
	else:
		serial_get = serial_get.split(' ')
		print serial_get
		if(not(int(serial_get[1]))):
			print "Warning"
		else:
			lista.append(int(serial_get[0]))
	if(count_pas>10):
		break
print lista
print count_pas
