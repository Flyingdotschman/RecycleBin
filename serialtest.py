import serial
from binascii import hexlify
from time import sleep

def starte_port():
    serialPort = serial.Serial('/dev/ttyS0')
    return serialPort


def set_sending_speed_500(port):
    data = "02 30 30 30 31 57 30 30 31 33 30 33 35 30 30 36 32 03"
    send_data(data,port)


def set_sending_speed_50(port):
    data = "02 30 30 30 31 57 30 30 31 33 30 32 35 30 36 32 03"
    send_data(data,port)



def start_sending(port):
    data = "02 30 30 30 31 45 31 30 31 31 30 30"
    send_data(data,port)

def stop_sending(port):
    data =  "02 30 30 30 31 45 31 30 31 30 30 30"
    send_data(data,port)



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
    gewicht = c*sign
    print(gewicht)


if __name__ == '__main__':
    serialPort = starte_port()

    try:
        set_sending_speed_500(serialPort)
        start_sending(serialPort)
        while 1:
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
    except KeyboardInterrupt:
        print("Program terminated manually!")
        stop_sending(serialPort)
        raise SystemExit



