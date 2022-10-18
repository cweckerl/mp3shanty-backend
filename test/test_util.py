from src.util import parse_date


def test_parse_date_valid():
  date_str = "2022-08-15T22:10:36.827Z"

  year, month, day = parse_date(date_str)

  assert year == 2022
  assert month == 8
  assert day == 15


def test_parse_date_invalid():
  date_str = "dummy"

  year, month, day = parse_date(date_str)

  assert year == -1
  assert month == -1
  assert day == -1
