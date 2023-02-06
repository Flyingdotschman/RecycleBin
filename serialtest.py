import serial

try:
    serialPort = serial.Serial('/dev/ttyS0')
except:
        tt = subprocess.Popen(["chmod", "666", "/dev/ttyS0"], stdout=subprocess.PIPE)
        serialPort = serial.Serial('/dev/ttyACM0')

data = "02 31 37 30 31 52 30 31 30 31 30 30"
data_in_bytes  = bytearray.fromhex(data)
print(data_in_bytes)
#data_in_bytes  = bytes.fromhex(data)

lrc = 0
for b in data_in_bytes[1:]:
    lrc ^= b
print(lrc)
print(lrc.bit_length())
print(data_in_bytes)
data_in_bytes.append(lrc)
x = bytes.fromhex('03')
data_in_bytes.extend(x)
print(data_in_bytes.hex())
data_in_bytes=bytearray.fromhex(data_in_bytes.hex())
print(data_in_bytes)
serialPort.write(data_in_bytes)
serialString = []

while 1:
    
    s_String = serialPort.read()
    

    serialString += s_String.decode('Ascii')
    s_String = serialPort.read(1)
print(serialString)    # Print the contents of the serial data
 
