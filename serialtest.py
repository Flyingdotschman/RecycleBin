import serial
from binascii import hexlify
from time import sleep
try:
    serialPort = serial.Serial('/dev/ttyS0')
except:
    tt = subprocess.Popen(["chmod", "666", "/dev/ttyS0"], stdout=subprocess.PIPE)
    serialPort = serial.Serial('/dev/ttyACM0')

data = "02 31 37 30 31 52 30 31 30 31 30 30"
ata = "02 30 30 30 31 52 30 31 30 37 30 30 30 30 03"
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


#data_in_bytes.append(lrc)
x = bytes.fromhex('03')
data_in_bytes.extend(x)
print(data_in_bytes.hex())
data_in_bytes=bytearray.fromhex(data_in_bytes.hex())
print(data_in_bytes)
print(len(data_in_bytes))
for b in data_in_bytes:
    print(chr(b))

#serialPort.write(bytearray.fromhex(ata))
while 1:
    serialPort.write(data_in_bytes)
    serialString = []
    s_String = []
    s_String = serialPort.readline()

    print(s_String)
    print(s_String[12:22])

    sleep(1)

