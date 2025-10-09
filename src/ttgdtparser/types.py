from abc import ABC
from datetime import time, datetime
from typing import Optional, Any, Tuple

from pydantic import BaseModel, ValidationError

from ttgdtparser.exc.parser import LessonIndexCantBeCorrectlyParsedException
from ttgdtparser.helpers import is_time


class BaseLesson(BaseModel, ABC):
    index: time | list[int] | str
    discipline: str
    teacher: Optional[str]
    room: Optional[str]

    def __init__(self, /, index: str, **data: Any) -> None:
        super().__init__(**data, index=index)
        self._normalize_index()

    def _normalize_index(self):
        if not isinstance(self.index, str):
            return

        try:
            cleaned_index = self._remove_non_numeric(self.index)

            translator = str.maketrans(r".,", ':' * 2)
            cleaned_index = cleaned_index.translate(translator)

            if cleaned_index.count(':') == 0:
                return

            if is_time(cleaned_index):
                self.index = self._parse_as_time(cleaned_index)
                return

            self.index = self._parse_as_number_list(cleaned_index)
        except (ValueError, ValidationError):
            raise LessonIndexCantBeCorrectlyParsedException()

    def _remove_non_numeric(self, index: str) -> str:
        import string
        allowed_chars = string.digits + '.,'
        return ''.join(char for char in index if char in allowed_chars)

    def _parse_as_time(self, time_repr: str) -> time:
        hour, minutes = list(map(int, time_repr.split(':')))
        return time(hour=hour, minute=minutes)

    def _parse_as_number_list(self, index: str) -> list[int]:
        return list(map(int, index.split(':')))


class Lesson(BaseModel, BaseLesson):
    by_even_weeks: Optional[bool] = False

    @property
    def has_difference(self):
        return self.change is not None


class Change(BaseModel, BaseLesson):
    date: datetime
    original: Lesson
    by_base: Optional[bool] = False


class Group(BaseModel):
    number: str


LessonMatch = Tuple[BaseLesson, BaseLesson]
