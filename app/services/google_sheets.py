import os.path

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def _authenticate():
    creds = None
    credentials = 'credentials.json'
    if os.path.exists(credentials):
        creds = service_account.Credentials.from_service_account_file(credentials)
    else:
        return None
    return build('sheets', 'v4', credentials=creds)


def get_spreadsheet_id_by_name(name: str):
    creds = None
    credentials = 'credentials.json'
    if os.path.exists(credentials):
        creds = service_account.Credentials.from_service_account_file(credentials)
    drive_service = build('drive', 'v3', credentials=creds)
    response = drive_service.files().list(
        q=f"name='{name}' and mimeType='application/vnd.google-apps.spreadsheet'",
        spaces='drive',
        fields='files(id, name)',
    ).execute()
    for file in response.get('files', []):
        if file.get('name') == name:
            return file.get('id')
    return None




def create_folder(name: str):
    creds, _ = google.auth.default()
    drive_service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = drive_service.files().create(body=file_metadata).execute()
    return folder.get('id')


def create(title: str, folder_name: str):
    creds, _ = google.auth.default()
    try:
        service = build("sheets", "v4", credentials=creds)
        folder_id = create_folder(folder_name)
        spreadsheet = {
            "properties": {"title": title},
            "parents": [folder_id]
        }
        spreadsheet = (
            service.spreadsheets()
            .create(body=spreadsheet, fields="spreadsheetId")
            .execute()
        )
        print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
        return spreadsheet.get("spreadsheetId")
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


class GoogleSheetsService:

    def __init__(self, sheet_name: str):
        self.sheet_name = sheet_name
        self.spreadsheet_id = get_spreadsheet_id_by_name(sheet_name)
        if self.spreadsheet_id is None:
            self.spreadsheet_id = create_new_sheet(sheet_name)
        self.client = _authenticate()

    def save_data(self, data: dict):
        try:
            values = [list(data.values())]
            body = {
                'values': values
            }
            result = self.client.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range="Sheet1!A1",
                valueInputOption="RAW",
                body=body
            ).execute()
            print(f"{result.get('updates').get('updatedCells')} cells appended.")
        except HttpError as e:
            print(f"An error occurred: {e}")
