file = open("test.txt", "r")

lista = []
count_pas = 0

while(True):
	serial_get = file.readline()
	if not (len(serial_get)):
		print "EOF"
		break 
	if(len(serial_get)>7):
		count_pas+=1
	else:
		serial_get = serial_get.split(' ')
		if(not(int(serial_get[1]))):
			#Not count
			print "Warning"
		else:
			lista.append(int(serial_get[0]))

print lista
print count_pas
