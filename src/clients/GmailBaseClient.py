import os, os.path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build


class GmailBaseClient:


    def __init__(self, scopes, user_id):
        self._scopes = scopes
        self._user_id = user_id


    def get_authenticated(self):
        """
            It authenticated the gmail api and store the credentials in instance private variable `_creds`
        """
        creds = None
        if os.path.exists('./creds/token.json'):
            creds = Credentials.from_authorized_user_file('./creds/token.json', self._scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('./creds/client_secrets.json', self._scopes)
                creds = flow.run_local_server(port=8001)
            with open('./creds/token.json', 'w') as token:
                token.write(creds.to_json())
        
        self._creds = creds
  

    def initialize_service(self):
        """
            It initializes the service in the instance private variable `_service`
        """
        try:
            service = build('gmail', 'v1', credentials=self._creds)
        except HttpError as error:
            print(f'An error occurred: {error}')

        self._service = service


    def get_user_mails(self, **kwargs):
        """
            Gets the query and return the filtered emails
        """
        kwargs.update({'userId': self._user_id})
        return self._service.users().messages().list(**kwargs).execute()


    def get_user_mail(self, id):
        """
            Gets unit mail and return the mail details form Gmail
        """
        return self._service.users().messages().get(userId=self._user_id, id=id).execute()
    

    def modify_email(self, **kwargs):
        """
            Moves email from one folder to other folder
        """
        return self._service.users().messages().modify(userId=self._user_id, **kwargs).execute()