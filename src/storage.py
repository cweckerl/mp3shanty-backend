import logging
from typing import Any

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
