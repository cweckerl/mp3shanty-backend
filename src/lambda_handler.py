import json
import logging
from typing import Any

from src.convert import convert
from src.storage import get_url, upload

log = logging.getLogger()
log.setLevel(logging.INFO)


def lambda_handler(event: dict, _: Any) -> dict:
  """Lambda handler for conversion request.

  Parameters
  ----------
  event: dict
    Input data to handler.
  _: LambdaContext
    Runtime information.

  Returns
  -------
  dict
    Json response
  """
  video_id = event["queryStringParameters"]["video_id"]
  filename = event["queryStringParameters"]["filename"]
  log.info(f"{video_id} received")

  path = convert(video_id, filename)
  mp3_id = upload(path)
  url = get_url(mp3_id)

  response = {
    "statusCode": 200,
    "headers": {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    },
    "body": json.dumps({"url": url}),
  }
  return response
