from abc import abstractmethod, ABC
from datetime import datetime
from typing import Any, Awaitable, Optional, List, Dict

from aiohttp import ClientSession, ClientResponse, ClientMiddlewareType
from bs4 import BeautifulSoup
from pydantic import validate_call, HttpUrl

from .constants import day_names, groups, raspisanie_zanyatij, zam, addictions
from .middleware import logging_middleware, validate_response_middleware
from .types import Lesson, Change, Group
from .utils import build_date_from_humaned, normilize_group_number


class BaseTtgdtWebsiteParser(ABC):
    _session: Optional[ClientSession] = None
    middlewares: List[ClientMiddlewareType] = [
        logging_middleware,
        validate_response_middleware
    ]

    def __init__(self, url: str, session: Optional[ClientSession] = None, *middlewares):
        self._session = session
        self.middlewares.extend(middlewares)
        self._url = url

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str):
        self._url = url

    @abstractmethod
    def parse(self, **kwargs) -> Awaitable[Any] | Any:
        raise NotImplementedError("Implement method 'parse' to fully close parser tasks")

    def initbs(self, response_body: str):
        return BeautifulSoup(response_body, 'lxml')

    def validate_response(self, response: ClientResponse):
        pass

    async def _ensure_session(self) -> ClientSession:
        if self._session is None:
            self._session = ClientSession(middlewares=self.middlewares)
        return self._session

    async def __aenter__(self):
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()


class LessonTableParser(BaseTtgdtWebsiteParser):
    @validate_call
    async def parse(self, group: str, date: Optional[datetime] = None):
        if date is None:
            date = datetime.now()

        session = await self._ensure_session()
        async with session.post(self.url, data={'gr_no': group}) as resp:
            html = await resp.text()
        bs = self.initbs(html)

        table = bs.select_one('table.table.table-striped.table-bordered')
        rows = table.find_all('tr')[1:]

        if date.weekday() > len(day_names) - 2:
            return []

        day = day_names[date.weekday()]
        found = False

        lessons = []

        for row in rows:
            tds = row.find_all('td')

            if len(tds) > 4:
                if found:
                    break

                if day != tds[0].get_text().lower():
                    continue
                else:
                    found = True

                tds = tds[1:]

            if not found or tds[1].get_text().strip() == "":
                continue

            if len(tds[0].get_text()) == 1:
                indx = tds[0].get_text()
                is_by_even = None
            else:
                indx = tds[0].get_text()[0]
                is_by_even = tds[0].get_text()[1].lower() == 'ч'

            lesson = Lesson(index=indx, by_even_weeks=is_by_even, discipline=tds[1].get_text(),
                            teacher=tds[2].get_text(), room=tds[3].get_text(), date=date)
            lessons.append(lesson)

        return lessons


class ChangesTableParser(BaseTtgdtWebsiteParser):
    async def parse(self, group: str = None) -> Dict[str, list["Change"]]:
        session = await self._ensure_session()
        async with session.get(self.url) as resp:
            html = await resp.text()
        bs = self.initbs(html)
        check_grp = group is not None

        tables = bs.select("table")

        changes: Dict[str, list["Change"]] = {}

        # get two tables and collect changes from it
        for table in tables:
            date = await build_date_from_humaned(table.find_previous('h1').get_text())

            rows = table.find_all('tr')[1:]
            current_group = None

            for row in rows:
                tds = row.find_all('td')

                if all(td.get_text() == "" for td in tds):
                    break

                grp = tds[0].get_text().strip()

                if grp != "":
                    if check_grp and group != grp:
                        current_group = None
                        continue

                    current_group = normilize_group_number(number=tds[0].get_text())
                    changes.setdefault(current_group, [])

                tds = tds[1:]

                change_discipline = tds[2].get_text().strip()
                by_base = change_discipline.lower() == 'по расписанию'

                if change_discipline == '-->':
                    change_discipline = tds[1].get_text().strip()

                indx = tds[0].get_text()
                change = Change(index=indx, date=date, discipline=change_discipline, room=tds[3].get_text(),
                                by_base=by_base)

                if current_group: 
                    changes.get(current_group).append(change)

        return changes


class GroupsParser(BaseTtgdtWebsiteParser):
    async def parse(self):
        session = await self._ensure_session()
        async with session.get(self.url) as resp:
            html = await resp.text()
        bs = self.initbs(html)

        groups_select = bs.find("select", {"id": "gr_no"})

        groups = []
        for select_option in groups_select.find_all("option")[1:]:
            option_value = select_option.attrs.get("value")
            groups.append(Group(number=option_value))

        return groups

    async def is_alive(self, group: str):
        grps = await self.parse()
        grps = [grp.number for grp in grps]
        return group in grps

class AddictionsParser(BaseTtgdtWebsiteParser):
    async def parse(self, date: Optional[datetime] = None):
        if date is None:
            date = datetime.now()
        
        if date.weekday() > len(day_names) - 2:
            return {}
        
        session = await self._ensure_session()
        async with session.get(self.url) as resp:
            html = await resp.text()
        bs = self.initbs(html)

        table = bs.select_one('table.table.table-striped.table-bordered')
        rows = table.find_all("tr")

        need_day = day_names[date.weekday()]
        current_group = None
        next_is_even = None
        addictions: Dict[str, List[Lesson]] = {}

        for row in rows:
            tds = row.find_all("td")
            if len(tds) == 0: continue
            if len(tds) == 1:
                group_header = row.find("span", {"style": "color:#ffffff;"})
                group_header_text = group_header.get_text().strip() if group_header else ""
                if not group_header_text: continue
                current_group = group_header_text
                addictions.setdefault(group_header_text, [])
                continue
            if len(tds) == 4 and current_group:

                day = tds[0].get_text().strip()
                if need_day in day.lower():
                    index = 0 if not "14.45-16.20" in day else 4
                    disciplines = tds[1].get_text().strip().replace('\t', '').split('\n')
                    teacher = tds[2].get_text().strip()
                    room = tds[3].get_text().strip().replace('а.', '')

                    if disciplines == ['']: continue
                    if len(disciplines) == 1:
                        lesson = Lesson(index=index, by_even_weeks=None, discipline=disciplines[0], teacher=teacher, room=room, date=date)
                        addictions[current_group].append(lesson)
                        continue
                    
                    for part in disciplines:
                        if "нечетная неделя" in part.lower():
                            next_is_even = False
                            continue 
                        elif "четная неделя" in part.lower():
                            next_is_even = True
                            continue
                        
                        lesson = Lesson(index=index, by_even_weeks=next_is_even, discipline=part, teacher=teacher, room=room, date=date)
                        addictions[current_group].append(lesson)
                        next_is_even = None
                
                

        return addictions


async def parse_addictions(date: Optional[datetime] = None, url: HttpUrl = None) -> Dict[str, List[Lesson]]:
    """
    Parse addictions from website
    :param date: date to get addictions (by default `datetime.now()`)
    :param url: url to get addictions (by default `ttgdtparser.constants.addictions()`)
    :return: list of addictions

    Usage:

        from ttgdtparser import parser, constants

        changes = await parser.parse_addictions(constants.addictions())
    """
    url = addictions() if url is None else url

    async with AddictionsParser(url) as parser:
        return await parser.parse(date=date)

async def parse_lessons(group: str, date: Optional[datetime] = None, url: HttpUrl = None) -> list[Lesson]:
    """
    Parse lessons from website
    :param group: group to get lessons
    :param date: date to get lessons (by default `datetime.now()`)
    :param url: url to get lessons (by default `ttgdtparser.constants.raspisanie_zanyatij()`)
    :return: list of lessons for group

    Usage:

        from ttgdtparser import parser, constants

        changes = await parser.parse_lessons(constants.raspisanie_zanyatij())
    """
    url = raspisanie_zanyatij() if url is None else url

    async with LessonTableParser(url) as parser:
        return await parser.parse(group=group, date=date)


async def parse_changes(group: str = None, url: HttpUrl = None) -> Dict[str, List[Change]]:
    """
    Parse changes from website
    :param group: group to get changes (optional)
    :param url: url to get changes (by default `ttgdtparser.constants.zam()`)
    :return: list of changes for all groups or for group if got

    Usage:

        from ttgdtparser import parser, constants

        changes = await parser.parse_changes(constants.zam())
    """
    url = zam() if url is None else url

    async with ChangesTableParser(url) as parser:
        return await parser.parse(group=group)


async def parse_groups(url: HttpUrl = None) -> List[Group]:
    """
    Parse from website select groups as option
    :param url: url to get select options with groups (by default `ttgdtparser.constants.groups()`)
    :return: list of groups

    Usage:

        from ttgdtparser import parser, constants

        groups = await parser.parse_groups(constants.groups())
    """
    url = groups() if url is None else url

    async with GroupsParser(url) as parser:
        return await parser.parse()


async def check_group_is_alive(group: str, url: HttpUrl = None) -> bool:
    """
    Check website select has a group number as option
    :param group: group to check
    :param url: url to get select options with groups (by default `ttgdtparser.constants.groups()`)
    :return: if group is presents by website return True

    Usage:

        from ttgdtparser import parser, constants

        is_alive = await parser.check_group_is_alive('711,722', constants.groups())
    """
    url = groups() if url is None else url

    async with GroupsParser(url) as parser:
        return await parser.is_alive(group)
