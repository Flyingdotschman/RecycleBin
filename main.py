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
from pynput.mouse import Controller as Mouse

delta_weight = 0
myduration = 20
gewicht_duration = 30000

debounce = False
debounce_time = 1

die_gpios = False
import mraa

die_gpios = True


def quit_me(e):
    root.quit()
    print("Quit")


def isplaying(player):
    # print(player.should_run)
    if player.should_run:
        if not player.is_Playing():
            print("Restart")
            player._Play()
        root.after(100, isplaying, player)


def start_waage():
    waage = threading.Thread(target=lese_waage)
    waage.start()


def quit_video(f, player):
    print("Video Killed")
    player._Quit()
    img = Image.open("/content/200/200grams_Conten_Gewicht_Einwurf-01.jpg")
    # img = Image.open("/home/pi/PeopleCounter_V3/Master.png")
    img = img.resize((400, 400), Image.ANTIALIAS)
    myimage = ImageTk.PhotoImage(img)
    #  mainCanvas = tk.Canvas(f)
    # mainCanvas.pack(fill='both', expand=True)
    mainCanvas.configure(bg="green")
    something = mainCanvas.create_image(0, 0, image=myimage, anchor=tk.NW)


def tuer(pin):
    global debounce
    debounce = True
    print(f"Tuer_Offen : {contentmanager.tuer_offen}")
    print(pin.read())
    old = pin.read()
    if pin.read() > 0:
        if not contentmanager.tuer_offen:
            tuer_auf()
            root.after(2000, checke_tuer_status, pin, old)
            return
    tuer_zu()
    root.after(2000, checke_tuer_status, pin, old)


def change_debounce():
    global debounce
    print(debounce)
    debounce = False


def tuer_auf():
    print("auf")
    contentmanager.tuer_auf()
    # contenmanager.tuer_offen = True
    waage.set_gewicht_anfang()


def checke_tuer_status(pin, old):
    global debounce
    debounce = False
    if pin.read() > 0:
        if not contentmanager.tuer_offen:
            tuer_auf()
            root.after(2000, checke_tuer_status, pin, old)
            return
    if not pin.read() > 0:
        if contentmanager.tuer_offen:
            tuer_zu()
            root.after(2000, checke_tuer_status, pin, old)
            return

    print("Alles ok")


def tuer_zu():
    # myduration = 3000
    print("zu")
    # waage.set_gewicht_ende()
    if contentmanager.tuer_offen:
        contentmanager.tuer_zu()
        # contenmanager.tuer_offen=False
        root.after(myduration, gewicht_routine)
    # contentmanager.show_weight_content(waage.delta_gewicht_lesen())


def gewicht_routine():
    contentmanager.show_weight_content(waage.delta_gewicht_lesen(), gewicht_duration)


def fakepin0(pin):
    pin.num0()
    tuer(pin)


def fakepin1(pin):
    pin.num1()
    tuer(pin)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    while True:
        try:
            # Set the TKinter Frames
            maus = Mouse()
            maus.position = (10000, 10000)
            os.chdir("/home/rock")
            try:
                updater = upd.Updater()
            except e:
                print("Something went wrong with the Content Update")
                print(f"The error was: {e}")
                sleep(8)

            root = tk.Tk()
            print(os.getcwd())
            print(os.getcwd())

            root.attributes("-fullscreen", True)
            #     root.geometry("600x400")

            # set Serial Connection
            # set GPIO Schalter
            pin = 8
            if die_gpios:
                pin = mraa.Gpio(pin)
                pin.dir(mraa.DIR_IN)
                pin.isr(mraa.EDGE_BOTH, tuer, pin)
                # pin.isr(mraa.EDGE_FALLING, tuer_zu, pin)
            else:

                class pin:
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
            waage = wg.Waage()
            print(waage.gewicht)
            contentmanager = cont.ContentManager(root)
            # Starte Player

            # Drucke Q fuer Quit
            root.bind("q", quit_me)
            #    root.bind(player.Event, player._Play, player)  #
            #   root.after(100, isplaying, player)

            root.mainloop()
        except:
            pass
