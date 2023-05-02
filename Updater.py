from sh import mount
import shutil
import os
from time import sleep

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
        #print(sda)
        if len(os.listdir("/media/USB")) > 0:
            self.mounted_check = True
        if not self.mounted_check:
            for f in sda:
                if "sd" in f :
                    print(f)
                    str = "/dev/" + f
                    mount(str, "/media/USB")
                    self.mounted_check = True
        if self.mounted_check:
            print("Found USB - Stick")
            sleep(1)
        if self.mounted_check:
            self.copydirec = os.listdir("/media/USB")
            for f in self.copydirec:
                if f == '0':
                    self.zero_check = True
                if f == 'offen':
                    self.offen_check = True
        print(f"Mounted: {self.mounted_check}")
        print(f"Found 0: {self.zero_check}")
        print(f"Found offen: {self.offen_check}")

        if self.mounted_check and self.zero_check and self.offen_check: 
            print("Also found  content folders, try to copy files...")
            sleep(1)
        if self.mounted_check and (self.zero_check and self.offen_check):
            self.olddirec = os.getcwd()
            self.olddirec = os.path.join(self.olddirec, "content")
            self.isthere = os.listdir(self.olddirec)
            onsucceed = True
            for f in self.copydirec:
                if f.isnumeric() or f=="offen":
                    print(f)

                    sleep(1)
                    print("*******************************")
                    try:        # Damit er nicht mehr abstuerzt und Magdalena den
                                # Dennis anruft
                        shutil.copytree(os.path.join("/media/USB", f), os.path.join(self.olddirec,f),dirs_exist_ok=True)
                    except Exception as  e:
                        files=os.listdir(os.path.join("/media/USB", f))
                        print(f"Error: Could not copy {files} in {f} !!!")
                        print(e)
                        sleep(5)
                        onsucceed = False
                        
                    else:
                        shutil.rmtree(os.path.join(self.olddirec,f))
                        print("Removed old content")
                        
                        shutil.copytree(os.path.join("/media/USB", f), os.path.join(self.olddirec,f),dirs_exist_ok=True)
                        print(f"Copied {f} successfully to to disk")
                        files=os.listdir(os.path.join("/media/USB", f))
                        print(f"Copied {f} successfully to to disk, Files: {files}")
                
            if onsucceed:
                for ff in self.isthere:
                    if ff not in self.copydirec:
                        shutil.rmtree(os.path.join(self.olddirec, ff))
                        print(f"Removed Old {ff}")
        print("START APPLICATION")
        sleep(5)

        

if __name__ == '__main__':
    updater = Updater()
    print("Start")
