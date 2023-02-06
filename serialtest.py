import serial
from binascii import hexlify
from time import sleep
try:
    serialPort = serial.Serial('/dev/ttyS0')
except:
    tt = subprocess.Popen(["chmod", "666", "/dev/ttyS0"], stdout=subprocess.PIPE)
    serialPort = serial.Serial('/dev/ttyACM0')

def set_sending_speed():
    data = "02 30 30 30 31 57 30 30 31 33 30 33 35 30 30 36 32 03"
    send_data(data)


#def start_sending():



def stop_sending():
    data =  "02 30 30 30 31 45 31 30 31 30 30 30"
    send_data(data)


def calc_lrc(data_in_bytes):
    lrc = 0
    for b in data_in_bytes[1:]:
    
        lrc ^= b
    lrc = str(lrc)
    return lrc


def send_data(data):
    data_in_bytes  = bytearray.fromhex(data)
    lrc = calc_lrc(data_in_bytes)
    for c in lrc:
        data_in_bytes.extend(c.encode())

    x = bytes.fromhex('03')
    data_in_bytes.extend(x)
    serialPort.write(data_in_bytes)

#data = "02 31 37 30 31 52 30 31 30 31 30 30"
#ata = "02 30 30 30 31 52 30 31 30 37 30 30 30 30 03"
data = "02 30 30 30 31 45 31 30 31 31 30 30"
data_in_bytes  = bytearray.fromhex(data)
print(data_in_bytes)
#data_in_bytes  = bytes.fromhex(data)

lrc = 0
for b in data_in_bytes[1:]:
    
    lrc ^= b
    print(lrc)

print(lrc)
print(lrc.bit_length())
print(data_in_bytes)
lrc = str(lrc)
for c in lrc:
    data_in_bytes.extend(c.encode())

print(lrc)

print(len(lrc))
stop_sending()

#data_in_bytes.append(lrc)
x = bytes.fromhex('03')
data_in_bytes.extend(x)
print(data_in_bytes.hex())
#data_in_bytes=bytearray.fromhex(data_in_bytes.hex())
print(data_in_bytes)
print(len(data_in_bytes))
for b in data_in_bytes:
    print(chr(b))

serialPort.write(data_in_bytes)
try:
    while 1:
  #  serialPort.write(data_in_bytes)
        serialString = []
        s_String = []
        s_String = serialPort.readline()
        print(s_String)
        print(s_String[12:22])

        sleep(1)
except KeyboardInterrupt:
   print("Program terminated manually!")
   stop_sending()
   raise SystemExit


