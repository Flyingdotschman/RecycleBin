from sh import mount
import shutil
import os

# Dieser Checkt ob auf dem USB die Ordner "0" und "offen" sind und kopiert dann
# alle Ordner auf den Rechner und dann ist der Content Up-to-Date
class Updater:

    def __init__(self):
        self.offen_check = False
        self.zero_check = False
        self.mounted_check = False
        self.copydirec = []
        self.olddirec = []
        sda = os.listdir("/dev/")
        print(sda)
        print(len(os.listdir("/media/USB")))
        if len(os.listdir("/media/USB")) > 0:
            self.mounted_check = True
        if not self.mounted_check:
            for f in sda:
                print(f)
                if "sd" in f and '1' in f:
                    str = "/dev/" + f
                    mount(str, "/media/USB")
                    self.mounted_check = True

        if self.mounted_check:
            self.copydirec = os.listdir("/media/USB")
            for f in self.copydirec:
                if f == '0':
                    self.zero_check = True
                if f == 'offen':
                    self.offen_check = True

        if self.mounted_check and (self.zero_check and self.offen_check):
            self.olddirec = os.getcwd()
            self.olddirec = os.path.join(self.olddirec, "content")
            shutil.rmtree(self.olddirec)
            os.mkdir(self.olddirec)
            for f in self.copydirec:
                try:        # Damit er nicht mehr abstuerzt und Magdalena den
                            # Dennis anruft
                    shutil.copytree(os.path.join("/media/USB", f), os.path.join(self.olddirec,f))
                except e:
                    pass
        print(self.mounted_check)
        print(self.zero_check)
        print(self.offen_check)


if __name__ == '__main__':
    updater = Updater()
    print("Start")