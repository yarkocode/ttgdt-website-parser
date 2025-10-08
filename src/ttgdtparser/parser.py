from datetime import datetime
from typing import Dict

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from pydantic import HttpUrl

from .constants import day_names
from .exceptions import WebsiteUnavailableException, NoTimetableAvailablePerDate
from .helpers import normilize_group_number, is_time
from .types import Lesson, Change, Group
from .utils import build_date_from_humaned


async def parse_lessons(url: HttpUrl, gr_no: str, date: datetime, secure: bool = True) -> list[Lesson]:
    """
    Parse lessons from common table
    :param url: endpoint with lessons table
    :param gr_no: number of the group
    :param date: date for which lessons should be parsed
    :param secure: use ssl checking

    :raises WebsiteUnavailableException: when the endpoint responds with a status non-eq. 200
    :raises NoTimetableAvailablePerDate: when the selected sunday

    :return: list of lessons by the date

    Usage:

    from ttgdtparser import parser, constants
    import datetime

    gr_no = "711,722"
    now = datetime.datetime.now()
    lessons = await parser.parse_lessons(constants.raspisanie_zanyatij(), gr_no, now)
    ...
    """
    async with ClientSession() as session:
        async with session.post(str(url), data={'gr_no': gr_no}, ssl=secure) as response:
            if response.status != 200:
                raise WebsiteUnavailableException(response.request_info)

            html_body = await response.text(encoding='utf-8')

        bs = BeautifulSoup(html_body, 'lxml')
        table = bs.select_one('table.table.table-striped.table-bordered')
        rows = table.find_all('tr')[1:]

        if date.weekday() > len(day_names) - 2:
            raise NoTimetableAvailablePerDate(response.request_info, "Requested date has not available lesson table")

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

            lesson = Lesson(date=date, index=indx, by_even=is_by_even, discipline=tds[1].get_text(),
                            teacher=tds[2].get_text(), room=tds[3].get_text())
            lessons.append(lesson)

        return lessons


async def parse_changes(url: HttpUrl, secure: bool = True) -> Dict[str, list[Change]]:
    """
    Parse changes
    :param secure: use ssl checking
    :param url: endpoint with changes table

    :raises WebsiteUnavailableException: when the endpoint responds with a status non-eq. 200

    :return: changes dict, group number as key

    Usage:

    from ttgdtparser import parser, constants

    changes = await parser.parse_changes(constants.zam())
    ...
    """
    async with ClientSession() as session:
        async with session.get(str(url), ssl=secure) as response:
            if response.status != 200:
                raise WebsiteUnavailableException(response.request_info)

            html_body = await response.text(encoding='utf-8')

    bs = BeautifulSoup(html_body, "lxml")
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

            group = tds[0].get_text().strip()

            if group != "":
                current_group = normilize_group_number(number=tds[0].get_text())
                changes[current_group] = []

            tds = tds[1:]

            change_discipline = tds[2].get_text().strip()
            by_base = change_discipline.lower() == 'по расписанию'

            if change_discipline == '-->':
                change_discipline = tds[1].get_text().strip()

            indx = tds[0].get_text()
            change = Change(index=indx, date=date, discipline=change_discipline, room=tds[3].get_text(),
                            by_base=by_base, index_is_time=is_time(indx))

            changes.get(current_group).append(change)

    return changes


async def parse_groups(url: HttpUrl, secure: bool = True) -> list[Group]:
    """
    Parse groups
    :param url: endpoint with groups select
    :param secure: use ssl checking

    :raises WebsiteUnavailableException: when the endpoint responds with a status non-eq. 200

    :return: list of group

    Usage:

    from ttgdtparser import parser, constants

    groups = await parser.parse_groups(constants.groups())
    ...
    """
    async with ClientSession() as session:
        async with session.get(str(url), ssl=secure) as response:
            if response.status != 200:
                raise WebsiteUnavailableException(response.request_info)

            html_body = await response.text(encoding='utf-8')

        bs = BeautifulSoup(html_body, 'lxml')
        groups_select = bs.find("select", {"id": "gr_no"})

        groups = []
        for select_option in groups_select.find_all("option")[1:]:
            option_value = select_option.attrs.get("value")
            groups.append(Group(full_number=option_value))

        return groups
