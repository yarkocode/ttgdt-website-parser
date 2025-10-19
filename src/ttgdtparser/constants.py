""" Parser constants """

MonthDict = dict[str, str]
DayDict = dict[str, int]

months: MonthDict = {
    'января': '01',
    'февраля': '02',
    'марта': '03',
    'апреля': '04',
    'мая': '05',
    'июня': '06',
    'июля': '07',
    'августа': '08',
    'сентября': '09',
    'октября': '10',
    'ноября': '11',
    'декабря': '12'
}

changes_date_start_index: int = 10
day_names: list[str] = [
    'понедельник',
    'вторник',
    'среда',
    'четверг',
    'пятница',
    'суббота',
    'воскресенье',
]

# parse urls
_website_base_url = "{protocol}://www.ttgdt.stu.ru"
_raspisanie_zanyatij = "/students/raspisanie-zanyatij"
_zam = "/students/zam"
_groups = "/students/raspisanie-zanyatij-ochnyh-otdelenij"
_addictions = "/students/raspisanie-dopolnitelnyh-zanyatij"

base_url = _website_base_url.format(protocol="https")
alternative_base_url = _website_base_url.format(protocol="http")


def _resolve_url(base: bool, endpoint: str) -> str:
    base = base_url if base else alternative_base_url
    return base + endpoint


raspisanie_zanyatij = lambda base=True: _resolve_url(base, _raspisanie_zanyatij)
zam = lambda base=True: _resolve_url(base, _zam)
groups = lambda base=True: _resolve_url(base, _groups)
addictions = lambda base=True: _resolve_url(base, _addictions)
