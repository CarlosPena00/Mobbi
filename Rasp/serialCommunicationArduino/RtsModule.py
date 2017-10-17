import serial

class RtsModule(object):
	"""docstring for RtsModule"""
	def __init__(self):
		self.ard = serial.Serial('/dev/ttyUSB0',9600)
 		self.lista_temp = []
 		self.lista_sound = []
 		self.lista_RFID = []
 		self.count_pass = 0
 		self.count_temp = 0
 		self.count_sound = 0

 	def getInformation():
 		st = self.ard.readline()
	    st = st.replace('\r\n','')
	    if('RFID' in st):
	        st = st.replace('RFID','')
	        self.lista_RFID.append(st)
	        self.count_pass+=1
	    elif ('UT' in st):
	        st = st.replace('UT ','')
	        st = st.split(' ')
	        if(len(st)>1):
	            if(isfloat(st[1])):
	                self.lista_temp.append(float(st[1]))
	                self.count_temp+=1
	    else:
	        st = st.split(' ')
	        if(len(st)>=2):
	            if(len(st[1])==1):
	                if(st[1] == '0'):
	                    print "warning"
	                else:
	                    if(st[0].isdigit()):
	                        self.lista_sound.append(int(st[0]))
	                        self.count_sound+=1
	    # print  st
	    med_temp = 0
	    med_sound = 0
	    for elemnt in self.lista_temp:
	        med_temp += elemnt
	    for elemnt in self.lista_sound:
	        med_sound += elemnt
	    result_med_temp = 0
	    result_med_sound = 0
	    if(count_temp>0):
	        result_med_temp = (med_temp)/count_temp
	    if(count_sound>0):
	        result_med_sound = (med_sound)/count_sound
		