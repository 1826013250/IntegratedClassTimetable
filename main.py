from tkinter import *
from sys import platform
import ctypes

from modules.custom_widgets import *
from modules.settings.general_settings import *
from modules.settings.classes_settings import *

ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)


class MyWindow(Tk):
    def __init__(self):
        super().__init__()
        self.version = "0.0"
        self.settings = load_settings(self)
        self.classes_settings = load_classes_settings()
        self.today = datetime.now().strftime("%A")
        self.tk.call('tk', 'scaling', ScaleFactor / 75)
        self.__decorate_window()
        self.__bind_events()
        self.need_resize = []
        self.__init_widgets()
        self.update()
        self.resize()
        self.__cycle_works()

    def resize(self, extra: list = None):
        wrootx = self.winfo_screenwidth() - self.winfo_width() - self.settings.window_pad[0] + self.settings.widget_pad
        wrooty = self.settings.window_pad[-1] - self.settings.widget_pad
        self.wm_geometry(f"+{wrootx}+{wrooty}")
        for widget in self.need_resize:
            widget.resize_work(wrootx, wrooty)
        if extra:
            for item in extra:
                item.resize_work(wrootx, wrooty)

    def __decorate_window(self):
        self.transparent_color = "#fffeff" if platform == "win32" else "grey"
        if platform == "win32":
            self.attributes("-transparentcolor", self.transparent_color)
        self.overrideredirect(True)
        self.config(bg=self.transparent_color)

    def __bind_events(self):
        self.bind("<Button-1>", lambda x: self.destroy())

    def __init_widgets(self):
        self.info = TextedRectangleReady(self, "info", self.settings.info)
        self.need_resize.append(self.info)
        title_day_frame = Frame(self)
        title_day_frame.pack()
        widget_height = self.settings.widget_heights["pairs"]
        widget_left_width = self.settings.widget_widths["pairs_left"]
        widget_right_width = self.settings.widget_widths["info"] - widget_left_width - 2 * self.settings.widget_pad
        self.day = TextedRectangleReady(self, "day", datetime.now().strftime("%A"), title_day_frame,
                                        width=widget_left_width, height=widget_height)
        self.need_resize.append(self.day)
        self.title_text = TextedRectangleReady(self, "title", self.settings.title, title_day_frame,
                                               width=widget_right_width, height=widget_height)
        self.need_resize.append(self.title_text)
        self.__create_classes()

    def __create_classes(self):
        self.classes_frames = []
        self.classes_times = []
        self.need_progress = {}
        print(self.classes_settings.get_daily().classes_raw)
        for item in self.classes_settings.get_daily():
            frame = Frame(self)
            frame.pack()
            self.classes_frames.append(frame)
            aclass = ProgressedTextedRectangleReady(
                self, "classes_name", item["classname"], self.settings.colors["classes_progress"],
                item["left"]["percentage"], frame,
                self.settings.widget_widths["info"] - self.settings.widget_widths["pairs_left"] -
                self.settings.widget_pad * 2,
                self.settings.widget_heights["pairs"]
            )
            self.need_progress[aclass] = item["self"]
            w = self.settings.widget_widths["pairs_left"]
            h = self.settings.widget_heights["pairs"]
            if item.get("no_time"):
                time = TextedRectangleReady(self,
                                            "classes_time",
                                            item["duration"],
                                            frame,
                                            w, h)
            else:
                time = TextedRectangleReady(self,
                                            "classes_time",
                                            item["duration"][0].strftime("%H:%M")
                                            + "\n" +
                                            item["duration"][-1].strftime("%H:%M"),
                                            frame,
                                            w, h)
            self.classes_times.append(time)

    def __delete_classes(self):
        for item in self.classes_frames:
            item.destroy()
        for item in self.classes_times:
            item.destroy()
        for item in self.need_progress.keys():
            item.destroy()
        self.classes_frames = []
        self.classes_times = []
        self.need_progress = {}

    def __refresh_progress(self):
        for widget, lesson in self.need_progress.items():
            widget.update_widget(progress=lesson.to_use()["left"]["percentage"])

    def __cycle_works(self):
        self.__insert_time()
        if datetime.now().strftime("%A") != self.today:
            self.__delete_classes()
            self.today = datetime.now().strftime("%A")
            self.__create_classes()
        self.resize(self.classes_times + list(self.need_progress.keys()))
        self.__refresh_progress()
        self.after(1000, self.__cycle_works)

    def __insert_time(self):
        self.info.update_widget(text=datetime.now().strftime(self.settings.info))


if __name__ == "__main__":
    app = MyWindow()
    app.mainloop()
