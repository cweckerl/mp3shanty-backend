import logging

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from src.credentials import get_client

log = logging.getLogger()


def upload(path: str) -> str:
  """Upload mp3 to storage.

  Parameters
  ----------
  path : str
    Path to mp3 file.

  Returns
  -------
  str
    ID of storage file.
  """
  try:
    service = get_client()

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


def get_url(id: str) -> str:
  """Creates download URL for mp3.

  Parameters
  ----------
  id : str
    ID of storage file.

  Returns
  -------
  str
    Download URL.
  """
  try:
    service = get_client()

    request_body = {"role": "reader", "type": "anyone"}
    service.permissions().create(fileId=id, body=request_body).execute()

    file = service.files().get(fileId=id, fields="webContentLink").execute()
  except HttpError as error:
    log.error(error)
    raise error

  return file.get("webContentLink")


def delete(id: str):
  """Delete file from storage.

  Parameters
  ----------
  id : str
    ID of storage file.
  """
  service = get_client()
  service.files().delete(fileId=id).execute()
  log.info(f"{id} deleted")
