from typing import Tuple, Union, List
from datetime import datetime, timedelta
from json5 import load, dump


class Class:
    def __init__(self,
                 content: dict,
                 tdi: List[dict],
                 cci: List[list],
                 cccs: int) -> None:
        self.content = content
        self.cycle_class_indexes = cci
        self.cycle_class_count_start =  cccs
        self.__name: str = content.get("name")
        self.cycle: bool = content.get("cycle")
        self.cycle_c_index: int = content.get("cycle_class_index")
        self.no_time: bool = content.get("no_time_duration")

        if content.get("time_duration_index"):
            self.begin_time = tdi[content["time_duration_index"]]["begin_time"]
            self.end_time = tdi[content["time_duration_index"]]["end_time"]
        else:
            self.begin_time = content.get("begin_time")
            self.end_time = content.get("end_time")

    def get_classname(self) -> str:
        if not self.cycle:
            return self.__name
        ...  # TODO: Cycle classes

    def get_duration(self) -> Union[Tuple[datetime, datetime], None]:
        if self.no_time:
            return None
        return datetime.strptime(self.begin_time, "%H:%M"), datetime.strptime(self.end_time, "%H:%M")

    def get_left(self, percentage: bool = False) -> Union[timedelta, float, None]:
        if self.no_time:
            return None
        now = datetime.now()
        begin, end = self.get_duration()
        begin.replace()
        if begin > now:
            if percentage:
                return 1
            return end - begin
        if end < now:
            if percentage:
                return 0
            return timedelta(0)
        if percentage:
            return (now - end).seconds / (end - begin).seconds
        return now - end

    def to_use(self, percentage: bool) -> dict:
        name = self.get_classname()
        duration = self.get_duration()
        left = self.get_left(percentage)
        return {
            "name": name,
            "duration": duration,
            "left": left
        }

    def to_save(self):
        return self.content


class ADay:
    def __init__(self,
                 day: str,
                 classes: list,
                 tdi: List[dict],
                 cci: List[list],
                 cccs: int) -> None:
        self.day = day
        self.__classes = []
        for _class in classes:
            self.__classes.append(Class(_class, tdi, cci, cccs))
        self.__num = -1

    def __iter__(self):
        self.__num = -1
        return self

    def __next__(self):
        self.__num += 1
        return self.__classes[self.__num].to_use()


class ClassesSettings:
    def __init__(self,
                 tdi: list = None,
                 cci: list = None,
                 cccs: datetime = datetime.strptime("", "")) -> None:
        ...
