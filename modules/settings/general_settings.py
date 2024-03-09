from json import dump, load, JSONDecodeError
from os.path import exists
from tkinter.messagebox import showerror
from sys import exit
from os import remove
from modules.utils import convert_font, export_font


class Settings:
    def __init__(self,
                 root,
                 window_pad: tuple = None,
                 fonts: dict = None,
                 widget_pad: int = 1,
                 widget_heights: dict = None,
                 widget_widths: dict = None,
                 colors: dict = None,
                 info: str = "%Y/%m/%d %a %H:%M",
                 title: str = "课程表",
                 debug: bool = False):
        self.root = root
        self.debug = debug
        
        if window_pad:  # 窗口边框间隔
            self.window_pad = window_pad
        else:
            self.window_pad = (0, 0)
        
        if fonts:  # 默认字体样式
            fonts_dict = {}
            for k, v in fonts.items():
                if v:
                    fonts_dict[k] = convert_font(root, v)
                else:
                    fonts_dict[k] = None
            self.fonts = fonts_dict
        else:
            self.fonts = {
                "info": convert_font(root, {"size": 20}),
                "title": convert_font(root, {"size": 25}),
                "day": convert_font(root, {"size": 25}),
                "classes_name": convert_font(root, {"size": 25}),
                "classes_time": convert_font(root, {"size": 20}),
            }
        
        self.widget_pad = widget_pad  # 组件之间间隔
        
        if widget_heights:
            self.widget_heights = widget_heights
        else:
            self.widget_heights = {
                "info": 60,
                "pairs": 60
            }
        
        if widget_widths:
            self.widget_widths = widget_widths
        else:
            self.widget_widths = {
                "info": 400,
                "pairs_left": 200
            }
        
        if colors:
            self.colors = colors
        else:
            self.colors = {
                "info_bg": ("black", .62),
                "info_fg": ("#c8c8c8", 1),
                "title_bg": ("black", .62),
                "title_fg": ("#c8c8c8", 1),
                "day_bg": ("black", .62),
                "day_fg": ("#c8c8c8", 1),
                "classes_time_bg": ("black", .6),
                "classes_time_fg": ("white", 1),
                "classes_name_bg": ("#5078c8", .2),
                "classes_name_fg": ("white", 1),
                "classes_progress": ("#c8c8c8", .62)
            }
        self.title = title
        self.info = info
    
        
def dict2class(adict, root):
    return Settings(
        root,
        adict["window_pad"],
        adict["fonts"],
        adict["widget_pad"],
        adict["widget_heights"],
        adict["widget_widths"],
        adict["colors"],
        adict["info"],
        adict["title"],
        adict["debug"]
    )
    
    
def class2dict(aclass: Settings):
    fonts_dict = {}
    for k, v in aclass.fonts.items():
        if v:
            fonts_dict[k] = export_font(v)
        else:
            fonts_dict[k] = None
    return {
        "window_pad": aclass.window_pad,
        "fonts": fonts_dict,
        "widget_pad": aclass.widget_pad,
        "widget_heights": aclass.widget_heights,
        "widget_widths": aclass.widget_widths,
        "colors": aclass.colors,
        "info": aclass.info,
        "title": aclass.title,
        "debug": aclass.debug
    }


def save_settings(settings: Settings):
    with open("settings.json", 'w', encoding="utf-8") as f:
        dump(settings, f, indent=2, default=class2dict, ensure_ascii=False)


def load_settings(root):
    if exists("settings.json"):
        try:
            with open("settings.json", 'r', encoding="utf-8") as f:
                return dict2class(load(f), root)
        except (JSONDecodeError, KeyError, TypeError):
            act = showerror("错误", "配置文件有误！\n"
                            "点击“是”将重置配置文件，请重新打开程序\n"
                            "点击“否”将关闭程序，请检查配置文件！",
                            type="okcancel")
            if act == "cancel":
                exit(-1)
            remove("settings.json")
            exit(0)
    else:
        settings = Settings(root)
        save_settings(settings)
        return settings
