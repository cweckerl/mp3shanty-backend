import logging
from datetime import datetime
from typing import Any
from src.util import parse_date, utc_now

from googleapiclient.errors import HttpError

log = logging.getLogger()


def delete(service: Any, id: str):
  """Delete file from storage.

  Parameters
  ----------
  service : Any
    Storage service client.
  id : str
    ID of storage file.
  """
  try:
    service.files().delete(fileId=id).execute()
    log.info(f"{id} deleted")
  except HttpError as error:
    log.error(error)
    raise error


def cleanup(service: Any, diff: int = 604800) -> int:
  """Removes files older than specified date.

  Parameters
  ----------
  service : Any
    Storage service client.
  diff: int, default=604800
    Minimum difference in seconds between file creation
    time and the current UTC time (One week in seconds).

  Returns
  -------
  int
    Number of files deleted.
  """
  try:
    response = service.files().list(fields="files(id, createdTime)").execute()
    files = response["files"]

    curr_date = utc_now()
    deleted = 0

    for f in files:
      year, month, day = parse_date(f["createdTime"])
      date = datetime(year, month, day)

      if (curr_date - date).total_seconds() > diff:
        delete(service, f["id"])
        deleted += 1

    log.info(f"{deleted} files deleted (Remaining: {len(files) - deleted})")
  except HttpError as error:
    log.error(error)
    raise error

  return deleted
  