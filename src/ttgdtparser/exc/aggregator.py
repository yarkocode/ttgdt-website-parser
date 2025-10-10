from ttgdtparser.types import Change


class AggregatorException(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message


class LessonRequiredByIndexForChangeException(AggregatorException):
    index: int | list[int]
    change: Change

    def __init__(self, message: str, index: int | list[int], change: Change):
        super().__init__(message)
        self.index = index
        self.change = change
