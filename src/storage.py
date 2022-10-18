import logging
from datetime import datetime
from typing import Any
from src.util import parse_date, utc_now

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

log = logging.getLogger()


def upload(service: Any, path: str) -> str:
  """Upload mp3 to storage.

  Parameters
  ----------
  service : Any
    Storage service client.
  path : str
    Path to mp3 file.

  Returns
  -------
  str
    ID of storage file.
  """
  try:
    metadata = {"name": path.split("/")[-1], "mimeType": "audio/mpeg"}
    media = MediaFileUpload(path, mimetype="audio/mpeg")

    file = (
      service.files()
      .create(body=metadata, media_body=media, fields="id")
      .execute()
    )
  except HttpError as error:
    log.error(error)
    raise error

  return file.get("id")


def get_url(service: Any, id: str) -> str:
  """Creates download URL for mp3.

  Parameters
  ----------
  service : Any
    Storage service client.
  id : str
    ID of storage file.

  Returns
  -------
  str
    Download URL.
  """
  try:
    request_body = {"role": "reader", "type": "anyone"}
    service.permissions().create(fileId=id, body=request_body).execute()

    file = service.files().get(fileId=id, fields="webContentLink").execute()
  except HttpError as error:
    log.error(error)
    raise error

  return file.get("webContentLink")


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


def sweep(service: Any, diff: int = 604800) -> int:
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
