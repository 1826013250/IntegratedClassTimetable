from tkinter.font import Font
from modules.custom_widgets import TextedRectangle


def convert_font(root, fontdict: dict):
    return Font(root,
                family=fontdict.get("fontname"),
                size=fontdict.get("size"),
                weight=fontdict.get("weight", "normal"),
                slant=fontdict.get("slant", "roman"),
                underline=fontdict.get("underline", False),
                overstrike=fontdict.get("overstrike", False))


def export_font(font: Font):
    base_dict = font.config()
    return {
        "fontname": base_dict["family"],
        "size": base_dict["size"],
        "weight": base_dict["weight"],
        "slant": base_dict["slant"],
        "underline": base_dict["underline"],
        "overstrike": base_dict["overstrike"]
    }
