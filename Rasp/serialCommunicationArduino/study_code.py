import serial
ard = serial.Serial('/dev/ttyUSB1',9600)
lista_temp = []
lista_Sound = []
lista_RFID = []
count_pass = 0
lista = []
i = 200
while i:
    st = ard.readline()
    st = st.replace('\r\n','')
    if('RFID' in st):
        st = st.replace('RFID','')
        lista_RFID.append(st)
        count_pass+=1
    elif ('UT' in st):
        st = st.replace('UT ','')
        st = st.split(' ')
        if(len(st)>1):
            lista_temp.append(float(st[1]))
    else:
        st = st.split(' ')
        if(len(st)>=2):
            if(len(st[1])==1):
                if(st[1] == '0'):
                    print "warning"
                else:
                    if(st[0].isdigit()):
                        lista_Sound.append(int(st[0]))
                        print "adicionado"
    print  st
    i-=1
print "Sound"
print lista_Sound
print "Temp"
print lista_temp
print "RFID"
print count_pass