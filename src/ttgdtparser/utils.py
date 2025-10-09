from datetime import datetime

from ttgdtparser.constants import changes_date_start_index, months

normilize_group_number = lambda number: number.strip().replace('.', ',')
normilize_group_number.__doc__ = """
Replace unsupported chars from string group number in changes
:param number: group number
:type number: str
:return: normalized group number string
"""


async def build_date_from_humaned(sdate: str) -> datetime:
    sdate = await _clean_humaned_date(sdate)
    date = datetime.strptime(sdate, "%d.%m.%Y")
    return date


async def _clean_humaned_date(sdate: str) -> str:
    sdate = sdate.strip()[changes_date_start_index:].replace('года', '')
    parts = sdate.split()
    parts[1] = months.get(parts[1])

    return ".".join(parts)
