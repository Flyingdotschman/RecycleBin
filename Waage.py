import serial
import subprocess
import threading

def calc_lrc(data_in_bytes):
        lrc = 0
        for b in data_in_bytes[1:]:
            lrc ^= b
        lrc=55
        lrc = str(lrc)
        print(lrc)
        return lrc


class Waage:
    def __init__(self):
        self.port = self.starte_port()
        self.gewicht_anfang = 0
        self.gewicht_ende = 0
        self.deltagewicht = 0
        self.gewicht = 0

    def starte_port(self):
        serialPort = serial.Serial('/dev/ttyS4')
        serialPort.baudrate = 9600
        serialPort.paritiy = serial.PARITY_NONE
        serialPort.stopbits = serial.STOPBITS_ONE
        serialPort.bytesize = serial.EIGHTBITS
        serialPort.timeout = 1
        return serialPort

    def lese_waage(self):
        self.send_data()
        serialSubString = self.read_data()
        self.read_gewicht(serialSubString)

    def send_data(self):
        data= "02 30 30 30 31 52 30 31 30 33 30 30"

        data_in_bytes  = bytearray.fromhex(data)
        lrc = calc_lrc(data_in_bytes)
        for c in lrc:
            data_in_bytes.extend(c.encode())

        x = bytes.fromhex('03')
        data_in_bytes.extend(x)
        self.port.write(data_in_bytes)

    
    def read_data(self):
        serialString=self.port.readline().decode('Ascii')
        serialSubString=serialString[12:21]
        print(serialSubString)
        return serialSubString


    def read_gewicht(self,serialSubstring):
        c = 0
        sign = 1
        print(f"Am Ende {serialSubstring[-1]}")

        if(serialSubstring[-1] == 'k'):
            for count, s in enumerate(serialSubstring):
               # print(s)
                if s == ' ':
                    s = '0'
                    continue
                if s == '-':
                    sign = -1 
                    print("MINUS!!!!")
                    continue
                if count == 4:
                    print(s)
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
        else:
            for count, s in enumerate(serialSubstring):
               # print(s)
                if s == ' ':
                    s = '0'
                    continue
                if s == '-':
                    sign = -1 
                    print("MINUS!!!!")
                    continue
                if count == 4:
                    print(s)
                if s.isnumeric(): 
                    if count == 3:
                        c += int(s) * 10
                        continue
                    if count == 4:
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

        print(f"Gewicht: {c * sign}"  )
        self.gewicht=c*sign
        print(f"self.Gewicht: {self.gewicht}")
     



    def waage_ablesen(self):
        self.lese_waage()
        print(self.gewicht)
        return self.gewicht

    def set_gewicht_anfang(self):
        self.gewicht_anfang = self.waage_ablesen()
        print(self.gewicht_anfang)

    def set_gewicht_ende(self):
        self.gewicht_ende = self.waage_ablesen()
        print(self.gewicht_ende)

    def delta_gewicht_lesen(self):
        self.set_gewicht_ende()
        self.deltagewicht = self.gewicht_ende - self.gewicht_anfang
        print(f"Anfang : {self.gewicht_anfang}")
        print(f"Ende: {self.gewicht_ende}")
        print(f'Delta Gewicht : {self.deltagewicht}')
        return self.deltagewicht

if __name__ == '__main__':
    waage = Waage()
    waage.set_gewicht_anfang()
    waage.set_gewicht_ende()
    waage.delta_gewicht_lesen()

