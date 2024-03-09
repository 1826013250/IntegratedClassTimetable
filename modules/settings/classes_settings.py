from typing import Tuple, Union, List
from datetime import datetime, timedelta
from os.path import exists
from os import remove
from tkinter.messagebox import showerror
from json5 import load, dump


class Class:
    def __init__(self,
                 content: dict,
                 tdi: List[dict],
                 cci: List[list],
                 cccs: datetime) -> None:
        self.content = content
        self.cycle_class_indexes = cci
        self.cycle_class_count_start = cccs
        self.__classname: str = content.get("classname")
        self.cycle: bool = content.get("cycle")
        self.cycle_c_index: int = content.get("cycle_class_index")
        self.no_time: bool = content.get("no_time_duration")
        self.style = content.get("style")
        self.custom_text = content.get("custom_text", "Untitled")

        if isinstance(content.get("time_duration_index"), int):
            self.begin_time = tdi[content["time_duration_index"]]["begin_time"]
            self.end_time = tdi[content["time_duration_index"]]["end_time"]
        else:
            self.begin_time = content.get("begin_time")
            self.end_time = content.get("end_time")

    def get_classname(self) -> str:
        if not self.cycle:
            return self.__classname
        ...  # TODO: Cycle classes

    def get_duration(self) -> Union[Tuple[datetime, datetime], None]:
        if self.no_time:
            return self.custom_text
        begin = datetime.strptime(self.begin_time, "%H:%M")
        end = datetime.strptime(self.end_time, "%H:%M")
        now = datetime.now()
        begin = begin.replace(now.year, now.month, now.day)
        end = end.replace(now.year, now.month, now.day)
        return begin, end

    def get_left(self) -> Union[dict, None]:
        if self.no_time:
            return {"percentage": 0, "timedelta": timedelta(0)}
        now = datetime.now()
        begin, end = self.get_duration()
        if begin > now:
            return {"percentage": 1, "timedelta": end - begin}
        if end < now:
            return {"percentage": 0, "timedelta": timedelta(0)}
        return {"percentage": (end - now).seconds / (end - begin).seconds, "timedelta": now - end}

    def to_use(self) -> dict:
        classname = self.get_classname()
        duration = self.get_duration()
        left = self.get_left()
        return {
            "classname": classname,
            "duration": duration,
            "left": left,
            "style": self.style,
            "no_time": self.no_time,
            "self": self
        }

    def to_save(self):
        return self.content


class ADay:
    def __init__(self,
                 classes: list,
                 tdi: List[dict],
                 cci: List[list],
                 cccs: datetime) -> None:
        self.classes_raw = classes
        self.__classes = []
        for _class in classes:
            self.__classes.append(Class(_class, tdi, cci, cccs))
        self.__num = -1

    def __iter__(self):
        self.__num = -1
        return self

    def __next__(self):
        self.__num += 1
        if self.__num >= len(self.__classes):
            raise StopIteration
        return self.__classes[self.__num].to_use()

    def to_save(self):
        return self.classes_raw


class ClassesSettings:
    def __init__(self,
                 classes: dict = None,
                 tdi: list = None,
                 cci: list = None,
                 cccs: str = "1900-01-01") -> None:
        if tdi:
            self.time_duration_indexes = tdi
        else:
            self.time_duration_indexes = []
        if cci:
            self.cycle_class_indexes = cci
        else:
            self.cycle_class_indexes = []
        self.cycle_class_count_start = datetime.strptime(cccs, "%Y-%m-%d")
        self.__classes = {}
        if classes:
            for k, v in classes.items():
                self.__classes[k] = ADay(v,
                                         self.time_duration_indexes,
                                         self.cycle_class_indexes,
                                         self.cycle_class_count_start)
        else:
            for k in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                self.__classes[k] = ADay([],
                                         self.time_duration_indexes,
                                         self.cycle_class_indexes,
                                         self.cycle_class_count_start)

    def get_daily(self, day: str = None) -> ADay:
        if day is None:
            day = datetime.now().strftime("%A")
        return self.__classes[day]

    def to_save(self) -> dict:
        classes = {}
        for k, v in self.__classes.items():
            classes[k] = v.to_save()
        return {
            "time_duration_indexes": self.time_duration_indexes,
            "cycle_class_indexes": self.cycle_class_indexes,
            "cycle_class_count_start": self.cycle_class_count_start.strftime("%Y-%m-%d"),
            "classes": classes
        }


def save_classes_settings(settings: ClassesSettings, path: str = "classes.json5"):
    with open(path, 'w', encoding="utf-8") as f:
        dump(settings.to_save(), f, ensure_ascii=False, indent=2)


def load_classes_settings(path: str = "classes.json5", debug: bool = False) -> ClassesSettings:
    if exists(path):
        try:
            with open(path, 'r', encoding="utf-8") as f:
                raw = load(f)
                return ClassesSettings(raw["classes"],
                                       raw["time_duration_indexes"],
                                       raw["cycle_class_indexes"],
                                       raw["cycle_class_count_start"])
        except (KeyError, TypeError, AttributeError, ValueError) as e:
            if debug:
                raise e
            act = showerror("错误", "课程文件有误！\n"
                            "点击“是”将重置课程文件，请重新打开程序\n"
                            "点击“否”将直接关闭程序，请检查配置文件！",
                            type="okcancel")
            if act == "cancel":
                exit(-1)
            remove(path)
            exit(0)
    else:
        settings = ClassesSettings()
        save_classes_settings(settings, path)
        return settings


if __name__ == "__main__":
    s = load_classes_settings("../../classes.json5", True)
    print(s)
    print(s.to_save())
    print(s.get_daily())
    for i in s.get_daily():
        print(i)
