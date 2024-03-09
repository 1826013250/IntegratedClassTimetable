from tkinter import Canvas, Toplevel, Wm
from tkinter.font import Font
from tkinter.ttk import Label, Frame
from typing import Union, Tuple, Literal


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
                 bgcolor: Tuple[str, float] = None,
                 fgcolor: Tuple[str, float] = None,
                 text: str = None,
                 font: str = None,
                 pad: int = 0,
                 transparent_color: str = None,
                 override_width: int = None,
                 override_height: int = None,
                 override_anchor: Literal["n", "s", "w", "e", "nw", "ne", "sw", "se"] = "") -> None:
        """创建一个包含文字的矩形

        Args:
            root (TkWindow): 传入一个window对象，可以是Tk，也可以是Toplevel
            placeholder (TkWidget): 传入一个组建对象，原组件作为占位符，获取长宽
            bgcolor (str, optional): 背景色，格式为settings. Defaults to None.
            fgcolor (str, optional): 前景色，格式为settings. Defaults to None.
            text (str, optional): 嵌入的文字. Defaults to None.
            font (str, optional): 文字样式. Defaults to None.
            pad (int, optional): 组件间距（边框大小）. Defaults to 0.
            transparent_color (str, optional): 窗口透明色. Defaults to None.
            override_width (int, optional): 覆写宽度而不是用placeholder的宽度
            override_height (int, optional): 同上
            override_anchor (str, optional): 在限定范围内矩形的对齐方式
        """
        self.root = root
        self.placeholder = placeholder
        self.full_width = placeholder.winfo_width()
        self.full_height = placeholder.winfo_height()
        width = override_width if override_width else placeholder.winfo_width()
        height = override_height if override_height else placeholder.winfo_height()
        self.width = width - pad * 2
        self.height = height - pad * 2
        self.bgcolor: Tuple[str, float] = bgcolor
        self.fgcolor: Tuple[str, float] = fgcolor
        self.text = text
        if font:
            self.font = font
        else:
            self.font = (None, 1)
        self.pad = pad
        self.transparent_color = transparent_color
        self.override_anchor = override_anchor
        self.__init_windows()
    
    def resize_work(self, x: int, y: int) -> None:
        """重置窗口位置

        Args:
            x (int): 占位符左上角的横坐标。
            y (int): 占位符左上角的纵坐标。
        """
        if "n" in self.override_anchor:
            pass
        elif "s" in self.override_anchor:
            y += self.full_height - self.height - 2 * self.pad
        if "w" in self.override_anchor:
            pass
        elif "e" in self.override_anchor:
            x += self.full_width - self.width - 2 * self.pad
        if self.width < 0:
            self.width = 0
        if self.height < 0:
            self.height = 0
        self.rectangle.wm_geometry(f"{self.width}x{self.height}"
                                   f"+{x + self.pad}+{y + self.pad}")
        self.text_window.wm_geometry(f"{self.width}x{self.height}"
                                     f"+{x + self.pad}+{y + self.pad}")
    
    def update_widget(self,
                      bgcolor: Tuple[str, int] = None,
                      fgcolor: Tuple[str, int] = None,
                      text: str = None,
                      font: Font = None,
                      pad: int = None,
                      override_width: int = None,
                      override_height: int = None,
                      override_anchor: str = None):
        """
        更新组件内容
        Args:
            bgcolor (Tuple[str, int], optional): 背景色
            fgcolor (Tuple[str, int], optional): 前景色
            text (str, optional): 更改的文字
            font (Font, optional): 更改的字体
            pad (int, optional): 更改的组件间距

        Returns:
            None
        """
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
        if override_anchor is not None:
            self.override_anchor = override_anchor
        if override_height is not None:
            self.height = override_height
        if override_width is not None:
            self.width = override_width

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

    def destroy(self) -> None:
        self.rectangle.destroy()
        self.text_window.destroy()

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


class TextedRectangleReady:
    def __init__(self, root, rec_type: str, text: str,
                 frame: Frame = None, width: str = None, height: str = None) -> None:
        """
        预配置的带文字的矩形
        Args:
            root ():
            rec_type ():
            text ():
            frame ():
        """
        self.root = root
        self.rec_type = rec_type
        self.text = text
        if width:
            self.width = width
        else:
            self.width = root.settings.widget_widths[rec_type]
        if height:
            self.height = height
        else:
            self.height = root.settings.widget_heights[rec_type]
        self.frame = frame
        self.placeholder = Canvas(frame if frame else root,
                                  bg=root.transparent_color if not root.settings.debug else "green",
                                  highlightthickness=0,
                                  width=self.width + root.settings.widget_pad * 2,
                                  height=self.height + root.settings.widget_pad * 2)
        self.placeholder.pack(anchor="e", side="right" if frame else "top")
        self.placeholder.update()
        self.rectangle = TextedRectangle(root,
                                         self.placeholder,
                                         root.settings.colors[rec_type+"_bg"],
                                         root.settings.colors[rec_type+"_fg"],
                                         text,
                                         root.settings.fonts[rec_type],
                                         root.settings.widget_pad,
                                         root.settings.colors[rec_type+"_bg"][0])

    def destroy(self) -> None:
        self.rectangle.destroy()
        self.placeholder.destroy()

    def resize_work(self, wrootx, wrooty) -> Tuple[int, int]:
        px = self.placeholder.winfo_x() + self.frame.winfo_x() if self.frame else 0
        py = self.placeholder.winfo_y() + self.frame.winfo_y() if self.frame else 0
        self.rectangle.resize_work(wrootx + px, wrooty + py)
        return px, py

    def update_widget(self, width=None, height=None, *args, **kwargs) -> None:
        if width:
            self.placeholder.configure(width=width)
        if height:
            self.placeholder.configure(height=height)
        self.rectangle.update_widget(*args, **kwargs)


class ProgressedTextedRectangleReady(TextedRectangleReady):
    def __init__(self,
                 root,
                 rec_type: str,
                 text: str,
                 progress_color: Tuple[str, float],
                 progress: float = 1,
                 frame: Frame = None,
                 width: str = None,
                 height: str = None) -> None:
        super().__init__(root, rec_type, text, frame, width, height)
        self.progress_color = progress_color
        self.progress = progress
        self.progress_mask = TextedRectangle(self.rectangle.rectangle,
                                             self.placeholder,
                                             self.progress_color,
                                             ("", 0),
                                             pad=self.root.settings.widget_pad,
                                             override_anchor="s",
                                             override_height=int(self.placeholder.winfo_height() * self.progress))

    def destroy(self) -> None:
        super().destroy()
        self.progress_mask.destroy()

    def update_widget(self, width=None, height=None, progress=None, progress_color=None, *args, **kwargs) -> None:
        super().update_widget(width, height, *args, **kwargs)
        if progress_color:
            self.progress_color = progress_color
        if progress is not None:
            self.progress = progress
            height = int((self.placeholder.winfo_height() - 2 * self.root.settings.widget_pad) * self.progress)
        else:
            height = int((self.placeholder.winfo_height() - 2 * self.root.settings.widget_pad) * self.progress)
        if self.progress <= 0:
            self.progress_mask.rectangle.wm_attributes("-transparentcolor", self.progress_color[0])
        else:
            self.progress_mask.rectangle.wm_attributes("-transparentcolor", None)
            self.progress_mask.update_widget(bgcolor=self.progress_color,
                                             override_height=height)

    def resize_work(self, wrootx, wrooty) -> Tuple[int, int]:
        px, py = super().resize_work(wrootx, wrooty)
        self.progress_mask.resize_work(wrootx + px, wrooty + py)
        return px, py
