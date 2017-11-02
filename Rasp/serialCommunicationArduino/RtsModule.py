import serial


class RtsModule(object):
    """docstring for RtsModule"""

    def __init__(self):
        self.ard = serial.Serial('/dev/ttyUSB0', 9600)
        self.lista_temp = []
        self.lista_sound = []
        self.lista_RFID = []
        self.count_pass = 0
        self.count_temp = 0
        self.count_sound = 0
        self.count_sound_warning = 0
        self.media_temp = 0

    def isfloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def getInfo(self):
        st = self.ard.readline()
        st = st.replace('\r\n', '')
        if('RFID' in st):
            st = st.replace('RFID', '')
            self.lista_RFID.append(st)
            self.count_pass += 1
        elif ('UT' in st):
            st = st.replace('UT ', '')
            st = st.split(' ')
            if(len(st) > 1):
                if(self.isfloat(st[1])):
                    self.lista_temp.append(float(st[1]))
                    self.count_temp += 1
        else:
            st = st.split(' ')
            if(len(st) >= 2):
                if(len(st[1]) == 1):
                    if(st[1] == '0'):
                        print "warning"
                    else:
                        if(st[0].isdigit()):
                            self.lista_sound.append(int(st[0]))
                            self.count_sound += 1

        # print  st
        med_temp = 0
        med_sound = 0

        for elemnt in self.lista_temp:
            med_temp += elemnt
        for elemnt in self.lista_sound:
            med_sound += elemnt
        result_med_temp = 0
        result_med_sound = 0
        if(self.count_temp > 0):
            result_med_temp = (med_temp) / self.count_temp
        if(self.count_sound > 0):
            result_med_sound = (med_sound) / self.count_sound
        if(result_med_sound > 30):
            self.count_sound_warning += 1

        self.media_temp = result_med_temp

        if(len(self.lista_temp) >= 1000):
            self.lista_temp = []
            self.count_temp = 0
        if(len(self.lista_sound) >= 1000):
            self.lista_sound = []
            self.count_sound = 0

    def getMsg(self):
        return self.count_pass, self.media_temp, self.count_sound_warning