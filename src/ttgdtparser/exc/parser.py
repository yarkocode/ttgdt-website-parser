from typing import Dict, Any

from ttgdtparser.exc.base import TtgdtWebsiteParserException


class ParserException(TtgdtWebsiteParserException):
    context: Dict[str, Any]

    def __init__(self, message: str, **context):
        super().__init__(message)
        self.context = context


class LessonIndexCantBeCorrectlyParsedException(ParserException):
    def __init__(self, message: str, **context):
        super().__init__(message, **context)


class WebsiteException(ParserException):
    def __init__(self, message: str, **context):
        super().__init__(message, **context)


class WebsiteSupportedContentNotFoundException(WebsiteException):
    def __init__(self, message: str, **context):
        super().__init__(message, **context)
