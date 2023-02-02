import serial
import subprocess
import threading
class Waage:
    def __init__(self, port):
        self.port = port
        self.waagethread = threading.Thread(target=self.lese_waage)
        self.waagethread.start()
        self.gewicht_anfang = 0
        self.gewicht_ende = 0
        self.deltagewicht = 0
        self.gewicht = 0

    def lese_waage(self):
        print("start_waage")
        while 1:
            serialString = []
            serialPort = self.port
            s_String = serialPort.read(1)
            try:
                while s_String != b'\r':
                    serialString += s_String.decode('Ascii')
                    s_String = serialPort.read(1)
                    # print(serialString)    # Print the contents of the serial data
                if len(serialString) == 13:
                    serialSubstring = []
                    serialSubstring = serialString[3:11]
                    # print(serialSubstring)
                    c = 0
                    for count, s in enumerate(serialSubstring):
                        if s == ' ':
                            s = '0'

                        if count == 2:
                            c += int(s) * 10

                        if count == 3:
                            c += int(s)
                        if count == 5:
                            c += int(s) * 0.1
                        if count == 6:
                            c += int(s) * 0.01
                        if count == 7:
                            c += int(s) * 0.001

                    self.gewicht = c
            except:
                self.gewicht = 0

    def waage_alive(self):
        if self.waagethread.is_alive():
            return True

    def waage_ablesen(self):
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
        print(self.deltagewicht)
        return self.deltagewicht

