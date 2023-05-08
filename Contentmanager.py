import os
import tkinter as tk
from tkinter import ttk

import Player as pl
from PIL import Image
from PIL import ImageTk


class ContentManager:
    def __init__(self, parent):

        self.tuer_offen = False

        self.pb = []        # Progressbar wenn Gewicht angezeigt wird
        self.myimage = []   # Platzhalter fuer Bild
        self.root = parent  # Frame bzw Canvas
        self.style = ttk.Style()    # Style fuer Progressbar w

        TROUGH_COLOR = 'black'
        BAR_COLOR = 'white'
        self.style.configure("bar.Horizontal.TProgressbar", troughcolor=TROUGH_COLOR,
                             bordercolor=TROUGH_COLOR, background=BAR_COLOR, lightcolor=BAR_COLOR,
                             darkcolor=BAR_COLOR)

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill='both', expand=True)
        self.mainCanvas = tk.Canvas(self.frame)
        self.mainCanvas.pack(fill='both', expand=True)
        self.imageThingy = self.mainCanvas.create_image(0, 0, image=[], anchor=tk.NW) # Platzhalter fuer image in Canvas
        # os.chdir('/home/dotsch/TBB')

        # Generiere ContentListe
        self.current_directory = os.getcwd()
        self.current_directory = os.path.join(self.current_directory, "content")
        dic_list = os.listdir(self.current_directory)
        dic_list.remove('offen')
        dic_list2=[]
        for i, f in enumerate(dic_list):

            try:
                f = int(f)
                dic_list[i] = f
                dic_list2.append(f)
            except:
                del dic_list[i]
        dic_list=dic_list2
        dic_list.sort()
        print(dic_list)
        self.dic_list = dic_list

        #Iinitialize Player
        self.player = []
        self.player = pl.Player()

        # Starte das erste Mal Dauercontent
        content = os.listdir(os.path.join(self.current_directory, '0'))
        print(content)
        print(content)

        for i, f in enumerate(content):
            if f.startswith('.'):
                continue
            break
        content = os.path.join(self.current_directory, '0', content[i])

        self.content = content
        self.content_type = self.video_or_image(self.content)
        self.content_should_run = True
        self.show_content()

    def video_or_image(self, file): # Ist Content type Video oder Bild
        video_extensions = ['.avi', '.mp4']
        image_extensions = ['.jpg', '.jpeg']
        filename, ext = os.path.splitext(file)
        e = ext.lower()
        # Only add common image types to the list.
        if e in video_extensions:
            return 'video'
        if e in image_extensions:
            return 'image'

    def show_content(self): # Zeige Content
        content_type = self.video_or_image(self.content)
        if content_type == 'video': # Wenn video
            self.player._Play_Media(self.content, self.mainCanvas)
            self.content_should_run = True
            self.root.after(100, self.isplaying)
            return
        #Wenn Bild
        img = Image.open(self.content)
        img = img.resize((1080, 1920))
        self.myimage = ImageTk.PhotoImage(img)
        self.mainCanvas.itemconfigure(self.imageThingy, image=self.myimage)
        print(self.mainCanvas.winfo_id())

    def run_dauer_content(self):  #Nicht mehr benoetigt
        if self.dauer_content_type == 'video':
            self.player = pl.Player(self.mainCanvas)
            self.player._Play_Media(self.dauer_content)
            self.dauer_content_should_run = True
            self.root.after(100, self.isplaying)
            return
        img = Image.open(self.dauer_content)
        img = img.resize((400, 400))
        self.myimage = ImageTk.PhotoImage(file=self.dauer_content)
        self.mainCanvas.configure(bg="blue")
        something = self.mainCanvas.create_image(0, 0, image=self.myimage, anchor=tk.NW)
        print(something)


# IsPlaying indentisch mit methide aus main.py, pruefen welche noetig ist
    def isplaying(self):
        # print(player.should_run)
        if self.content_should_run:

            if not self.player.is_Playing():
                print("Restart")
                self.player._Play()
            self.root.after(100, self.isplaying)

    def change_content(self, new_content):
        try:
            self.pb.destroy()
        except:
            pass
        content = os.listdir(os.path.join(self.current_directory, new_content))
        # print(content)
        for i, f in enumerate(content):
            if f.startswith('.'):
                continue
            break
        content = os.path.join(self.current_directory, new_content, content[i])
        if content == self.content:
            print("Same content")
            return
        print("Changing Content:  " + content)
        self.content = content

        self.stop_content()
        self.show_content()

    def stop_content(self):
        if self.content_type == 'video':
            self.content_should_run = False
            self.player._Quit()
            return
        self.mainCanvas.itemconfigure(self.imageThingy, image=[])

    def show_weight_content(self, weight, show_duration):
        if self.tuer_offen:
            return
        k = 0
        weight = weight * 1000
        print(f'weight contentmanager : {weight}')
        for i, w in enumerate(self.dic_list):
            if weight >= w:
                k = i
                print(w)
                print(i)

        print("Show weight")
        if k> 0:
            self.change_content(str(self.dic_list[k]))
            this_length = 1080
            self.pb = ttk.Progressbar(self.mainCanvas, style="bar.Horizontal.TProgressbar", orient=tk.HORIZONTAL,
                                      length=this_length, mode='determinate')
            self.pb.pack()

            self.pb.start(int(show_duration/100))
            print("Set After Timer")
            self.mainCanvas.after(show_duration, self.reset_view)
        else:
            self.change_content('0')

    def reset_view(self):
        if not self.tuer_offen:
            self.change_content('offen')
            self.change_content('0')

    def tuer_auf(self):
        self.change_content('offen')
        self.tuer_offen=True

    def tuer_zu(self):
        self.tuer_offen=False


if __name__ == "__main__":
    root = tk.Tk()
    # root.geometry("600x400")
    content_manager = ContentManager(root)

    root.mainloop()
