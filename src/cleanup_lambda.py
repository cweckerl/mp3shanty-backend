import json
import logging

from src.credentials import get_service
from src.delete import cleanup

log = logging.getLogger()
log.setLevel(logging.INFO)


def lambda_handler(event: dict, _) -> dict:
  """Lambda handler for cleanup request.

  Parameters
  ----------
  event: dict
    Input data to handler.

  Returns
  -------
  dict
    Json response
  """
  log.info("Beginning cleanup")

  service = get_service()
  n = cleanup(service)

  response = {
    "statusCode": 200,
    'body': json.dumps(f"{n} files deleted")
  }
  return response
