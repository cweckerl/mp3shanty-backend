import re
from datetime import datetime
from typing import Tuple


def utc_now() -> datetime: return datetime.utcnow()


def parse_date(date: str) -> Tuple[int, int, int]:
  """Parses date string into tuple form of date.

  Parameters
  ----------
  date : str
    RFC 3339 datetime string (although other formats
    will be matched).

  Returns
  -------
  Tuple[int, int, int]
    Tuple of year, month, day
  """
  p = re.compile(r"(\d{4})\-(\d{2})\-(\d{2})T")
  if m := p.search(date):
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
  return (-1, -1, -1)
  