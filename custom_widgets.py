from tkinter import Canvas, CENTER, Toplevel, Wm
from tkinter.ttk import Label, Frame
from typing import Union, List


class TransparentToplevel(Toplevel):
    """透明窗口"""
    def __init__(self, *args,
                 alpha: float = 1.0,
                 root_top: bool = True,
                 transparent: Union[bool, str] = False,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.master: Wm = args[0]
        self.alpha = alpha
        self.root_top = root_top
        self.transparent = transparent
        self.wm_attributes("-alpha", self.alpha)
        self.wm_attributes("-transparentcolor", self.transparent) if isinstance(self.transparent, str) else None
        self.transient(self.master) if self.root_top else None
    
    def set_alpha(self, new_alpha: float) -> None:
        """设置透明度

        Args:
            new_alpha (float): 透明度数值
        """
        self.alpha = new_alpha
        self.wm_attributes("-alpha", new_alpha)
    
    def set_bg(self, new_bg: str) -> None:
        """设置背景色

        Args:
            new_bg (str): 背景颜色
        """
        self.configure(bg=new_bg)


class BorderlessTransparentToplevel(TransparentToplevel):
    def __init__(self, *agrs, **kwargs):
        """透明无边框窗口"""
        super().__init__(*agrs, **kwargs)
        self.wm_overrideredirect(True)


class TextedRectangle:
    def __init__(self,
                 root,
                 placeholder,
                 bgcolor: str = None,
                 fgcolor: str = None,
                 text: str = None,
                 font: str = None,
                 pad: int = 0,
                 transparent_color=None) -> None:
        """创建一个包含文字的矩形

        Args:
            root (TkWindow): 传入一个window对象，可以是Tk，也可以是Toplevel
            placeholder (TkWidget): 传入一个组建对象，原组件作为占位符，获取长宽
            bgcolor (str, optional): 背景色，格式为settings. Defaults to None.
            fgcolor (str, optional): 前景色，格式为settings. Defaults to None.
            text (str, optional): 嵌入的文字. Defaults to None.
            font (str, optional): 文字样式. Defaults to None.
            pad (int, optional): 组件间距（边框大小）. Defaults to 0.
            transparent_color (_type_, optional): 窗口透明色. Defaults to None.
        """
        self.root = root
        self.placeholder = placeholder
        self.width = placeholder.winfo_width() - pad * 2
        self.height = placeholder.winfo_height() - pad * 2
        self.bgcolor: List[str, float] = bgcolor
        self.fgcolor: List[str, float] = fgcolor
        self.text = text
        self.font = font
        self.pad = pad
        self.transparent_color = transparent_color
        self.__init_windows()
    
    def resize_work(self, x: int, y: int) -> None:
        """重置窗口位置

        Args:
            x (int): 窗口左上角的横坐标。
            y (int): 窗口左上角的纵坐标。
        """
        self.rectangle.wm_geometry(f"{self.width}x{self.height}"
                                   f"+{x + self.pad}+{y + self.pad}")
        self.text_window.wm_geometry(f"{self.width}x{self.height}"
                                     f"+{x + self.pad}+{y + self.pad}")
    
    def update_widget(self, bgcolor=None, fgcolor=None, text=None, font=None, pad=None):
        if bgcolor:
            self.bgcolor = bgcolor
        if fgcolor:
            self.fgcolor = fgcolor
        if text:
            self.text = text
        if font:
            self.font = font
        if pad:
            self.pad = pad

        self.text_label.configure(text=self.text,
                                  font=self.font,
                                  foreground=self.fgcolor[0],
                                  background=self.transparent_color)
        self.text_antialiasing.configure(text=self.text,
                                         font=self.font,
                                         foreground=self.fgcolor[0],
                                         background=self.bgcolor[0])
        self.rectangle.set_bg(self.bgcolor[0])
        self.rectangle.set_alpha(self.bgcolor[-1])
        if self.fgcolor[-1] <= 0.5:
            self.text_antialiasing.configure(text="")
        else:
            self.text_antialiasing.configure(text=self.text)

    def __init_windows(self) -> None:
        self.rectangle = BorderlessTransparentToplevel(self.root,
                                                       alpha=self.bgcolor[-1],
                                                       bg=self.bgcolor[0])
        self.text_antialiasing = Label(self.rectangle,
                                       text=self.text,
                                       font=self.font,
                                       foreground=self.fgcolor[0],
                                       background=self.bgcolor[0])
        self.text_window = BorderlessTransparentToplevel(self.root,
                                                         alpha=self.fgcolor[-1],
                                                         bg=self.transparent_color,
                                                         transparent=self.transparent_color)
        self.text_label = Label(self.text_window,
                                text=self.text,
                                font=self.font,
                                foreground=self.fgcolor[0],
                                background=self.transparent_color)
        self.text_antialiasing.place(relx=.5, rely=.5, anchor="center")
        if self.fgcolor[-1] <= 0.5:
            self.text_antialiasing.configure(text="")
        self.text_label.place(relx=.5, rely=.5, anchor="center")


class RectangleReady:
    def __init__(self, root, rec_type: str, text: str, frame: Frame = None) -> None:
        self.root = root
        self.rec_type = rec_type
        self.text = text
        self.placeholder = Canvas(frame if frame else root,
                                  bg=root.transparent_color if not root.settings.debug else "green",
                                  highlightthickness=0,
                                  width=root.settings.widget_widths[rec_type] + root.settings.widget_pad * 2,
                                  height=root.settings.widget_heights[rec_type] + root.settings.widget_pad * 2)
        self.placeholder.pack(anchor="e", side="right" if frame else "top")
        self.placeholder.update()
        self.rectangle = TextedRectangle(root,
                                         self.placeholder,
                                         root.settings.colors[rec_type+"_bg"],
                                         root.settings.colors[rec_type+"_fg"],
                                         text,
                                         root.settings.fonts[rec_type],
                                         root.settings.widget_pad,
                                         root.transparent_color)

    def resize_work(self, wrootx, wrooty) -> None:
        self.rectangle.resize_work(wrootx + self.placeholder.winfo_x(), wrooty + self.placeholder.winfo_y())

    def update_widget(self, width=None, height=None, *args, **kwargs) -> None:
        if width:
            self.placeholder.configure(width=width)
        if height:
            self.placeholder.configure(height=height)
        self.rectangle.update_widget(*args, **kwargs)
