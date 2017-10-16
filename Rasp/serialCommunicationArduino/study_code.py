import serial

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

ard = serial.Serial('/dev/ttyUSB0',9600)
lista_temp = []
lista_Sound = []
lista_RFID = []
count_pass = 0
lista = []
i = 200
count_temp = 0
count_sound = 0
while True:
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
            if(isfloat(st[1])):
                lista_temp.append(float(st[1]))
                count_temp+=1
    else:
        st = st.split(' ')
        if(len(st)>=2):
            if(len(st[1])==1):
                if(st[1] == '0'):
                    print "warning"
                else:
                    if(st[0].isdigit()):
                        lista_Sound.append(int(st[0]))
                        count_sound+=1
    # print  st
    med_temp = 0
    med_sound = 0
    for elemnt in lista_temp:
        med_temp += elemnt
    for elemnt in lista_Sound:
        med_sound += elemnt
    result_med_temp = 0
    result_med_sound = 0
    if(count_temp>0):
        result_med_temp = (med_temp)/count_temp
    if(count_sound>0):
        result_med_sound = (med_sound)/count_sound

    print "Data: "+str(count_pass)+","+ str(result_med_temp)+", ("+str(result_med_sound)+" , "+str(len(lista_Sound))+")"
# print "Sound"
# print lista_Sound
# print "Temp"
# print lista_temp
# print "RFID"
# print count_pass