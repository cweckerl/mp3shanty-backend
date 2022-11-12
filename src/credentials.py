import os
import random

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def get_service():
  """Get API client from service account.

  Returns
  -------
  Any
    Object for interacting with Drive service.
  """
  SCOPES = ["https://www.googleapis.com/auth/drive"]
  n = random.randint(0, 2)
  if n == 0:
    serv_account = "creds1.json"
  elif n == 1:
    serv_account = "creds2.json"
  else:
    serv_account = "creds3.json"
  SERVICE_ACCOUNT_FILE = os.path.join(serv_account)
  creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  return build("drive", "v3", credentials=creds)
