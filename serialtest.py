import serial
from binascii import hexlify
from time import sleep

def starte_port():
    serialPort = serial.Serial('/dev/ttyS0')
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



def set_weight_unit(port):
    print("set_weight_unit")
#    data= "02 30 30 30 31 57 30 30 32 30 30 32 30 32"
    data_s= "02 30 30 30 31 57 30 30 32 30 30 32 "
    for d in range(0,9):
        for c in range(0,9):
    

            for a in range(0,9):
                for b in range(0,9):
                    t1=(str(d)+str(c))
                    t2=(str(a)+str(b))
                    t3=t1+' '+t2
                    data = data_s +t3 
                    print(data)
                    send_data(data,port)
                    strung=serialPort.readline().decode('Ascii')
                    if len(strung) > 11:
                        #print(strung[12])
                        if strung[12]!='3':
                            print('*********************** Achtung ******************************')
                            print(strung)
                            print(f' Hex : {a}{b}') 
        #            print(serialPort.readline().decode('Ascii'))
        #            print(serialPort.readline().decode('Ascii'))
        #            sleep(1)

def get_max_weight(port):
    print("get_max_weight m1")
    data= "02 30 30 30 31 52 30 30 32 32 30 30"
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
    lrc = str(lrc)
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
    for i in range(100):
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



if __name__ == '__main__':
    serialPort = starte_port()

    try:
        get_weight_unit(serialPort)
        set_weight_unit(serialPort)
        #get_range_mode(serialPort)
        #get_max_weight(serialPort)
        get_weight_value(serialPort)
        #get_seal_status(serialPort)
    except KeyboardInterrupt:
        print("Program terminated manually!")
        stop_sending(serialPort)
        raise SystemExit

    stop_sending(serialPort)


