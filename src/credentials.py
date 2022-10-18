import os

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
  SERVICE_ACCOUNT_FILE = os.path.join("creds.json")
  creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  return build("drive", "v3", credentials=creds)
