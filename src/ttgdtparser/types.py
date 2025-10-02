from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class Lesson(BaseModel):
    date: datetime
    index: str
    discipline: str
    by_even: Optional[bool] = None
    teacher: Optional[str] = None
    room: Optional[str] = None
    change: Optional["Change"] = None

    @property
    def has_difference(self) -> bool:
        return self.change is not None


class Change(Lesson, BaseModel):
    discipline: Optional[str] = None
    by_base: Optional[bool] = False
    index_is_time: bool = False

    @property
    def subindexation(self):
        if self.index_is_time:
            return []

        return self.index.split(",")



class Group(BaseModel):
    full_number: str

    @property
    def subgroups(self) -> List[str]:
        parted = self.full_number.split(",")
        if len(parted) < 2:
            return []
        return parted

    @property
    def has_subgroups(self) -> bool:
        return len(self.subgroups) > 0
