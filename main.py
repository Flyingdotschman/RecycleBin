import vlc
import Contentmanager as cont
import tkinter as tk
import threading
import serial
from PIL import Image
from PIL import ImageTk
import subprocess
import os
import Waage as wg
import Updater as upd
from time import sleep
from tkinter import ttk
from pynput.mouse import Controller as Maus

# delta_weight = 0

myduration = 2000  # Dauer zwischen Klappe zu und Content, damit die Waage Zeit zum Wiegen hat in MS
gewicht_duration = 30000  # Dauer die der Gewichtcontent angezeigt wird in MS
nummer_sicher_gpio = 500  # Dauer nach der der Gpio erneut ausegelesen werden soll.

debounce = False  # Debounce
debounce_time = 1  # Debounce Timer in Sekunden

die_gpios = False  # Sind wir auf einem Rock Pi mit GPIOs?
try:

    import mraa  # Fuer GPIOS

    die_gpios = True
except ImportError:
    print("UPs")
    die_gpios = False


def quit_me(e):  # Programm zu beenden, funkioniert nicht
    root.quit()
    print("Quit")


# Ist is playing noetig? Siehe Cotentmanager
def isplaying(player):  # Chechkob Video Player laeuft
    # print(player.should_run)
    if player.should_run:  # Soll der Player laufen?

        if not player.is_Playing():  # Falls er laufen soll, tut es aber nicht -> Restart
            print("Restart")
            player._Play()
        root.after(100, isplaying, player)  # Checke alle 0,1 Sekunden, ob der Player laeuft


def start_waage():  # starte Kommunikatio mit der Waage NICHT MEHR BENOETIGT
    waage = threading.Thread(target=lese_waage)
    waage.start()


def quit_video(f, player):  # ALT kann raus
    print("Video Killed")
    player._Quit()
    img = Image.open("/content/200/200grams_Conten_Gewicht_Einwurf-01.jpg")
    # img = Image.open("/home/pi/PeopleCounter_V3/Master.png")
    img = img.resize((400, 400), Image.ANTIALIAS)
    myimage = ImageTk.PhotoImage(img)
    #  mainCanvas = tk.Canvas(f)
    # mainCanvas.pack(fill='both', expand=True)
    mainCanvas.configure(bg='green')
    something = mainCanvas.create_image(0, 0, image=myimage, anchor=tk.NW)


def tuer(pin):  # Callback fuer Tuer GPIO
    global nummer_sicher_gpio
    global debounce
    print(debounce)
    if not debounce:  # Timer fuer Button debounce
        debounce = True
        root.after(1000, change_debounce)
        a = pin.read()
        root.after(nummer_sicher_gpio, read_tuer_oncemore, a,
                   pin)  # Lese nach einer Sekunde erneut den GPIO um sicher zu gehen


def read_tuer_oncemore(a, pin):  # Lese GPIO erneut
    if a == pin.read():  # Wenn der GPIO der gleiche Wert wie vorher, dann mache etwas
        if pin.read() > 0:  # entscheide ob Tuer auf oder zu gegangen ist
            tuer_auf()
            return
        tuer_zu()


def change_debounce():  # setze DEbounce zurueck
    global debounce

    print(debounce)
    debounce = False


def tuer_auf():  # Tuer geht auf, zeige offen Content und messe Gewicht
    print("auf")
    contentmanager.tuer_auf()
    waage.set_gewicht_anfang()


def tuer_zu():  # Tuer zu,
    # myduration = 3000
    print("zu")
    # waage.set_gewicht_ende()
    contentmanager.tuer_zu()  # sage dem Contentmanager, dass die tuer zu ist
    root.after(myduration, gewicht_routine)  # warte nach dem schliesen der tuer myduration um zu wiegen
    # damit die Waage zeit hat sich einzupendeln


def gewicht_routine():
    contentmanager.show_weight_content(waage.delta_gewicht_lesen(), gewicht_duration)
    # schicke Gewicht an Contentmanager und zeige das Gewicht an solange gewicht_duration


def fakepin0(pin):
    pin.num0()
    tuer(pin)


def fakepin1(pin):
    pin.num1()
    tuer(pin)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Move Mouse out of the Way
    maus = Maus()
    maus.position = (10000, 10000)

    os.chdir('/home/rock/TBB')  # Set working directory

    updater = upd.Updater()  # Starte USB Updater

    # Set the TKinter Frames
    root = tk.Tk()

    root.attributes('-fullscreen', True)
    # root.geometry("600x400")

    # set Serial Connection
    try:
        serialPort = serial.Serial('/dev/ttyACM0')
    except:
        tt = subprocess.Popen(["chmod", "666", "/dev/ttyACM0"], stdout=subprocess.PIPE)
        print("Popen")
        print(tt)
        serialPort = serial.Serial('/dev/ttyACM0')

    # set GPIO Schalter
    pin = 8
    if die_gpios:
        pin = mraa.Gpio(pin)
        pin.dir(mraa.DIR_IN)
        pin.isr(mraa.EDGE_BOTH, tuer, pin)
        # pin.isr(mraa.EDGE_FALLING, tuer_zu, pin)
    else:
        class pin():
            num = 1

            def __init__(self):
                self.num = 1

            def read(self):
                return self.num

            def num1(self):
                self.num = 1

            def num0(self):
                self.num = 0


        pin = pin()
        root.bind("x", lambda eff: fakepin0(pin))
        root.bind("c", lambda eff: fakepin1(pin))
    # Starte Waage
    waage = wg.Waage(serialPort)
    print(waage.gewicht)
    contentmanager = cont.ContentManager(root)
    # Starte Player

    # Drucke Q fuer Quit
    root.bind("q", quit_me)

    root.mainloop()
