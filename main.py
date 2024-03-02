from tkinter import *
from tkinter.ttk import *
from sys import platform
import ctypes
from datetime import datetime

from custom_widgets import *
from settings import *
from utils import *

ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)


class MyWindow(Tk):
    def __init__(self):
        super().__init__()
        self.version = "0.0"
        self.settings = load_settings(self)
        self.tk.call('tk', 'scaling', ScaleFactor / 75)
        self.__decorate_window()
        self.__bind_events()
        self.need_resize = []
        self.__init_widgets()
        self.update()
        self.resize()
        self.__cycle_works()

    def resize(self):
        wrootx = self.winfo_screenwidth() - self.winfo_width() - self.settings.window_pad[0] + self.settings.widget_pad
        wrooty = self.settings.window_pad[-1] - self.settings.widget_pad
        self.geometry(f"+{wrootx}+{wrooty}")
        for widget in self.need_resize:
            widget.resize_work(wrootx, wrooty)

    def __decorate_window(self):
        self.transparent_color = "#fffeff" if platform == "win32" else "grey"
        if platform == "win32":
            self.attributes("-transparentcolor", self.transparent_color)
        self.overrideredirect(True)
        self.config(bg=self.transparent_color)

    def __bind_events(self):
        self.bind("<Button-1>", lambda x: self.destroy())

    def __init_widgets(self):
        self.info = RectangleReady(self, "info", self.settings.info)
        self.need_resize.append(self.info)
        self.title = RectangleReady(self, "title", self.settings.title)
        self.need_resize.append(self.title)

    def __cycle_works(self):
        self.__insert_time()
        self.resize()
        self.after(1000, self.__cycle_works)

    def __insert_time(self):
        self.info.update_widget(text=datetime.now().strftime(self.settings.info))


if __name__ == "__main__":
    app = MyWindow()
    app.mainloop()
