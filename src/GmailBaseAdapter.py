import os, os.path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build


class GmailBaseAdapter:
    
  def __init__(self, scopes, user_id):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    self.scopes = scopes
    self.creds = self.get_authenticate()
    self.service = self.initialize_service()
    self.user_id = user_id

  def get_authenticate(self):
    # Authenticate Gmail API
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./creds/token.json'):
        creds = Credentials.from_authorized_user_file('./creds/token.json', self.scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './creds/client_secret.json', self.scopes)
            creds = flow.run_local_server(port=8001)
        # Save the credentials for the next run
        with open('./creds/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds
  
  def initialize_service(self):
    try:
        return build('gmail', 'v1', credentials=self.creds)

    except HttpError as error:
        print(f'An error occurred: {error}')