import serial
from binascii import hexlify
from time import sleep
from time import time as clock

def starte_port():
    serialPort = serial.Serial('/dev/ttyS2')
    serialPort.baudrate = 9600
    serialPort.paritiy = serial.PARITY_NONE
    serialPort.stopbits = serial.STOPBITS_ONE
    serialPort.bytesize = serial.EIGHTBITS
    serialPort.timeout = 1
    return serialPort


def set_sending_speed_500(port):
    data = "02 30 30 30 31 57 30 30 31 33 30 33 35 30 30 36 32 03"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))



def set_sending_speed_50(port):
    data = "02 30 30 30 31 57 30 30 31 33 30 32 35 30 36 32 03"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))

def start_sending(port):
    data = "02 30 30 30 31 45 31 30 31 31 30 30"
    send_data(data,port)
    read_stream2(port)
 


def start_sending2(port):
    data = "02 30 30 30 31 45 31 30 31 31 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    read_stream(port)

def get_seal_status(port):
    print("get_seal_status")
    data= "02 30 30 30 31 52 30 30 30 39 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))

def get_all(port):
    print("get_all")
    data= "02 30 30 30 31 45 41 41 41 41 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))

def set_weight_unit_v1(port):
    print("ChatGPT")
    data= "02 30 30 30 31 57 30 30 32 30 30 32 4B 47"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))


def set_weight_unit(port):
    start=clock()
    vorhin=start
    print("set_weight_unit")
#    data= "02 30 30 30 31 57 30 30 32 30 30 32 30 32"
    data= "02 30 30 30 31 57 30 30 32 30 30 31 "
    

   # for b in range(0,65535):
    for a in range(47,58):
        jetzt=clock()
        gesamt=jetzt-start
        durch = jetzt - vorhin
        vorhin = jetzt
        print(f'Durchlauf {a}; Gesamt: {gesamt}, Zeit pro Durchlauf: {durch}')

    #for b in range(0,255):
#        print(f'a={a} und b={b}')
        data_in_bytes  = bytearray.fromhex(data)
        t1=a.to_bytes(1,'big')
     #   t2=b.to_bytes(1,'big')
        data_in_bytes.extend(t1)
#        print(data_in_bytes)
      #  data_in_bytes.extend(t2)
        lrc = calc_lrc(data_in_bytes)
        for c in lrc:
            data_in_bytes.extend(c.encode())
 
        x = bytes.fromhex('03')
        data_in_bytes.extend(x)
#        print(data_in_bytes)
        serialPort.write(data_in_bytes)

        #print(f'Frage : {data_in_bytes}')
        strung=serialPort.readline().decode('Ascii')
        if len(strung) > 11:
#                print(f'Frage : {data_in_bytes}')

            print(f'Falsche Antwort {strung}')
            #print(strung[12])
            if strung[12]!='3':
                print('*********************** Achtung ******************************')
                print(f'Antwort bekommen: {strung}; Frage: {data_in_bytes} mit {a}')
                get_weight_value(port)
                get_weight_unit(port)
#            print(serialPort.readline().decode('Ascii'))
#            print(serialPort.readline().decode('Ascii'))
#            sleep(1)

def get_max_weight(port):
    print("get_max_weight m1")
    data= "02 30 30 30 31 52 30 30 32 32 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print("get_max_weight e1")
    data= "02 30 30 30 31 52 30 30 32 33 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))

    
    print(serialPort.readline().decode('Ascii'))
    print("get_max_weight m2")
    data= "02 30 30 30 31 52 30 30 32 34 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))

    print(serialPort.readline().decode('Ascii'))
    print("get_max_weight e2")
    data= "02 30 30 30 31 52 30 30 32 35 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))


def set_max_weights(port):
    print('Setting Maximum Weights')
    print('Setting max1')
    data_m1="02 30 30 30 31 57 30 30 32 32 30 35 33 30 30 30 30"
    send_data(data_m1,port)
    print(serialPort.readline().decode('Ascii'))

    print('Setting e1')
    data_e1="02 30 30 30 31 57 30 30 32 33 30 31 35"
    send_data(data_e1,port)
    print(serialPort.readline().decode('Ascii'))
    print('Setting max2')
    data_m2="02 30 30 30 31 57 30 30 32 34 30 38 36 30 30 30 30 30 30 30"
    send_data(data_m2,port)
    print(serialPort.readline().decode('Ascii'))



def get_status(port):
    print("get_status")
    data= "02 30 30 30 31 52 30 31 30 30 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))



def get_weight_unit(port):
    print("get_weight_unit")
    data= "02 30 30 30 31 52 30 30 32 30 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))


def get_weight_value(port):
    print("get_weight_value")
    data= "02 30 30 30 31 52 30 31 30 33 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))

def get_tare(port):
    print("get_tare")
    data= "02 30 30 30 31 52 30 31 30 32 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))

def get_scale_adj(port):
    print('init_zero')
    data= "02 30 30 30 31 52 30 30 33 30 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))

    print('slope')
    data= "02 30 30 30 31 52 30 30 33 31 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))

    print('precal')
    data= "02 30 30 30 31 52 30 30 33 32 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))

def get_zero_indicator(port):
    print('precal')
    data= "02 30 30 30 31 52 30 31 30 35 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))

def set_scale_adj(port):
    print('init_zero')
    data= "02 30 30 30 31 57 30 30 33 30 30 35 34 30 34 34 32"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))

    print('slope')
    data= "02 30 30 30 31 57 30 30 33 31 30 36 31 30 32 30 35 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))


def do_initial_adj(port):
    print('intial zero adj')
    data =  "02 30 30 30 31 45 31 30 33 30 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))

def span_adj(port):
    print('span adj')
    data =  "02 30 30 30 31 45 31 30 33 31 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))



def get_number_of_pieces(port):
    print("get_number_of_pieces")
    data= "02 30 30 30 31 52 30 31 30 39 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))

def get_range_mode(port):
    print("get_range_mode")
    data= "02 30 30 30 31 52 30 30 32 38 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))


def get_weight_value_for_adjust(port):
    print("get_weight_value_for_adjust")
    data= "02 30 30 30 31 52 30 30 33 34 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))

def set_weight_value_for_adjust(port):
    print("set_weight_value_for_adjust")
    data= "02 30 30 30 31 57 30 30 33 34 30 35 32 30 30 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))



def stop_sending(port):
    data =  "02 30 30 30 31 45 31 30 31 30 30 30"
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))


def send_factory_reset(port):
    data =  "02 30 30 30 31 45 31 30 30 33 30 30"
    data =  "02 30 30 30 31 45 45 45 45 45 30 30" 
    send_data(data,port)
    sleep(2)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))

def reset_device(port):
    print("reset_device")
    data =  "02 30 30 30 31 45 39 39 39 39 30 30" 
    send_data(data,port)
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))
    print(serialPort.readline().decode('Ascii'))




def calc_lrc(data_in_bytes):
    lrc = 0
    for b in data_in_bytes[1:]:
        lrc ^= b
    lrc=55
    lrc = str(lrc)
    print(lrc)
    return lrc


def send_data(data,serialPort):
    data_in_bytes  = bytearray.fromhex(data)
    lrc = calc_lrc(data_in_bytes)
    for c in lrc:
        data_in_bytes.extend(c.encode())

    x = bytes.fromhex('03')
    data_in_bytes.extend(x)
    print(data_in_bytes)
    serialPort.write(data_in_bytes)


def read_gewicht(serialSubstring):
    c = 0
    sign = 1
    for count, s in enumerate(serialSubstring):
        s=chr(s) 
       # print(s)
        if s == ' ':
            s = '0'
            continue
        if s == '-':
            sign = -1 
            print("MINUS!!!!")
            continue
        if s.isnumeric(): 
            if count == 2:
                c += int(s) * 10
                continue
            if count == 3:
                c += int(s)
                continue
            if count == 5:
                c += int(s) * 0.1
                continue
            if count == 6:
                c += int(s) * 0.01
                continue
            if count == 7:
                c += int(s) * 0.001
                continue
        print(c)
    gewicht = c*sign*4
    print(gewicht)
    

def read_stream(port):
    while True:
        serialString = []
        s_String = []
        s_String = serialPort.readline()
        print(s_String)
        serialSubstring=s_String[13:21]
        print(serialSubstring)
        read_gewicht(serialSubstring)

        try:
            read_gewicht(serialSubstring)
        except:
            pass


def read_stream2(port):
    while True:
        string2=port.read()


        if string2 == '\n':
            print('Neue Zeile')
        print(string2)

if __name__ == '__main__':
    serialPort = starte_port()

    try:
       # set_scale_adj(serialPort)
       # get_scale_adj(serialPort)

#        do_initial_adj(serialPort)
#        get_zero_indicator(serialPort)
        get_weight_value(serialPort)
        start_sending2(serialPort)
    except KeyboardInterrupt:
        print("Program terminated manually!")
        stop_sending(serialPort)
        raise SystemExit

    stop_sending(serialPort)


