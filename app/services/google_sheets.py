import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class GoogleSheetsService:

    def __init__(self, credentials: str, spreadsheet_id: str):
        self.credentials = credentials
        self.spreadsheet_id = spreadsheet_id
        self.client = self._authenticate()

    def _authenticate(self):
        creds = None
        if os.path.exists(self.credentials):
            creds = Credentials.from_authorized_user_file(self.credentials, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.credentials, 'w') as token:
                token.write(creds.to_json())
        return build('sheets', 'v4', credentials=creds)

    def save_data(self, data: dict):
        try:
            # Open the spreadsheet
            spreadsheet = self.client.spreadsheets()
            # Select the first sheet
            sheet = spreadsheet.values()
            # Append the data to the sheet
            values = [list(data.values())]
            body = {
                'values': values
            }
            result = sheet.append(spreadsheetId=self.spreadsheet_id, range="Sheet1!A1",
                                  valueInputOption="RAW", body=body).execute()
            print(f"{result.get('updates').get('updatedCells')} cells appended.")
        except HttpError as e:
            print(f"An error occurred: {e}")
