import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def auth():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def list_files(service):
    page_token = None
    while True:
        param = {}
        if page_token:
            param['pageToken'] = page_token
        files = service.files().list(pageSize=10).execute()
        # print(files)
        return files['files']

def view():
    drive_service = auth()
    xx = []
    for x in list_files(drive_service):
        fid = "https://drive.google.com/uc?export=download&id=" + x['id']
        xx.append({
            'name': x['name'],
            'download_link': fid,
            'id': x['id']
        })
        print(f'Name: {x["name"]}, Link: {fid}')
    # print(xx)


view()
