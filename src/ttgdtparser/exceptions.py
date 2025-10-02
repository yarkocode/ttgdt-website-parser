from aiohttp import RequestInfo


class ParserException(Exception):
    def __init__(self, message: str, context: RequestInfo):
        self.message = message
        self.context = context


class WebsiteUnavailableException(ParserException):
    def __init__(self, context: RequestInfo, message: str = "Website unavailable"):
        super().__init__(message, context)


class TableNotFoundExceptionOnAvailablePage(ParserException):
    def __init__(self, context: RequestInfo, message: str = "Table not found on available page"):
        super().__init__(message, context)


class NoTimetableAvailablePerDate(ParserException):
    def __init__(self, context: RequestInfo, message: str = "No timetable available per date"):
        super().__init__(message, context)