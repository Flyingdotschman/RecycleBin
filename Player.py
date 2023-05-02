import vlc
import tkinter as tk

class Player:

    def __init__(self):
        # tk.Frame.__init__(self, parent)
        self.parent = []
        self.media = []
        # self.videoPanel = tk.Frame(self.parent)
        #self.canvas = tk.Canvas(self.parent)
        #self.canvas.pack(fill=tk.BOTH, expand=1)
        # self.videoPanel.pack(fill=tk.BOTH, expand=1)
        self.should_run = []
        #self.h = self.canvas.winfo_id()
        args = ['--no-xlib', '--input-repeat=-999999']
        self.Instance = vlc.Instance(args)
        self.player = self.Instance.media_player_new()
        self.Event = vlc.EventType.MediaPlayerEndReached
        # h = self.videoPanel.winfo_id()
        #self.player.set_xwindow(self.h)

    def setvideo(self, video):
        self.media = self.Instance.media_new(str(video))
        self.player.set_media(self.media)
        a = self.Instance.vlm_set_loop(str(video), True)
        print(a)

    def _Play(self):
        self.player.set_media(self.media)
        self.player.play()
        self.should_run = True

    def _Play_Media(self, video,parent):
        self.parent = parent
        #self.canvas = tk.Canvas(self.parent)
        #self.canvas.pack(fill=tk.BOTH, expand=1)
        self.canvas=parent
        self.h = self.canvas.winfo_id()
        print(self.canvas.winfo_id())
        self.media = self.Instance.media_new(str(video))
        self.player.set_media(self.media)
        self.player.set_xwindow(self.h)
        self.player.play()
        self.should_run = True
    def is_Playing(self):
        if self.player.is_playing():
            return True

    def _Quit(self):
        self.parent.configure(bg="black")
        self.should_run = False
        self.player.stop()
        #self.canvas.destroy()
    #    self.parent.destroy()
    # self.player.quit()


