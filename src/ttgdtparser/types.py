from datetime import time, datetime
from typing import Optional, Any, Tuple, Union

from pydantic import BaseModel, ValidationError, ConfigDict, field_validator

from ttgdtparser.exc.parser import LessonIndexCantBeCorrectlyParsedException
from ttgdtparser.helpers import is_time


class BaseLesson(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    date: datetime
    index: list[int] | int | time | str
    discipline: str
    teacher: Optional[str] = None
    room: Optional[str] = None

    @field_validator("index", mode="before")
    @classmethod
    def normalize_index(cls, index: str | int) -> int | list[int] | time:
        if isinstance(index, int) or isinstance(index, list) or isinstance(index, time):
            return index

        if not isinstance(index, str):
            raise ValidationError("Index must be str or int")

        cleaned_index = cls._remove_non_numeric(index)

        translator = str.maketrans(r".,", ':' * 2)
        cleaned_index = cleaned_index.translate(translator)

        try:
            if cleaned_index.count(':') == 0:
                return int(cleaned_index)

            if is_time(cleaned_index):
                return cls._parse_as_time(cleaned_index)

            return cls._parse_as_number_list(cleaned_index)
        except (ValueError, ValidationError):
            raise LessonIndexCantBeCorrectlyParsedException(
                f"Lesson index has invalid format to parse: {cleaned_index}")

    @staticmethod
    def _remove_non_numeric(index: str) -> str:
        import string
        allowed_chars = string.digits + '.,'
        return ''.join(char for char in index if char in allowed_chars)

    @staticmethod
    def _parse_as_time(time_repr: str) -> time:
        hour, minutes = list(map(int, time_repr.split(':')))
        return time(hour=hour, minute=minutes)

    @staticmethod
    def _parse_as_number_list(index: str) -> list[int]:
        return list(map(int, index.split(':')))


class Lesson(BaseLesson, BaseModel):
    by_even_weeks: Optional[bool] = False


class Change(BaseLesson, BaseModel):
    original: Optional[Lesson] = None
    by_base: Optional[bool] = False


class Group(BaseModel):
    number: str


LessonMatch = Tuple[BaseLesson, BaseLesson]
