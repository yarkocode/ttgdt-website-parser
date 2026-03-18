import logging
from datetime import datetime

from .constants import changes_date_start_index, months

logger = logging.getLogger(__name__)

normilize_group_number = lambda number: number.strip().replace('.', ',').replace(' ', '')
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
    sdate = sdate.strip()[changes_date_start_index:].replace('года', '').strip()
    parts = sdate.split()

    if len(parts) < 3:
        raise ValueError(f"Unexpected date format: '{sdate}' (expected at least 3 parts: day month year)")

    month = months.get(parts[1])
    if month is None:
        raise ValueError(f"Unknown month '{parts[1]}' in date string '{sdate}'")

    parts[1] = month
    return ".".join(parts)