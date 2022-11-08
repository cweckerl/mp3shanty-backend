import json
import logging

from src.convert import convert
from src.credentials import get_service
from src.storage import get_url, upload

log = logging.getLogger()
log.setLevel(logging.INFO)


def lambda_handler(event: dict, _) -> dict:
  """Lambda handler for conversion request.

  Parameters
  ----------
  event: dict
    Input data to handler.

  Returns
  -------
  dict
    Json response
  """
  video_id = event["queryStringParameters"]["video_id"]
  title = event["queryStringParameters"]["title"]
  artist = event["queryStringParameters"]["artist"]

  log.info(f"{video_id} received")

  path = convert(video_id, title, artist)
  service = get_service()
  mp3_id = upload(service, path)
  url = get_url(service, mp3_id)

  response = {
    "statusCode": 200,
    "headers": {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    },
    "body": json.dumps({"url": url}),
  }
  return response
