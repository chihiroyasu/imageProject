import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# Google Drive APIのスコープ
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
    
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_folder_files(folder_id):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    # フォルダ内のファイル情報を取得
    results = service.files().list(q=f"'{folder_id}' in parents",
                                   fields="files(id, name)").execute()
    files = results.get('files', [])

    if not files:
        print('No files found.')
    else:
        # print('Files:')
        # for file in files:
        #     print(f"Name: {file['name']}, ID: {file['id']}, Type: {file['mimeType']}")
        return files
            
def download_file(real_file_id, name):
    try:
        creds = authenticate()
        service = build('drive', 'v3', credentials=creds)
    
        file_id = real_file_id
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while not done:
                # チャンクごとにファイルをダウンロード
                status, done = downloader.next_chunk()
                # ダウンロードの進行状況を表示
                print(f"ダウンロード進行状況: {int(status.progress() * 100)}%")
    
        destination = os.path.expanduser("~/yasu_device/temp")
        file_name = name
        file_path = os.path.join(destination, file_name)
    
        with open(file_path, "wb") as f:
            f.write(file.getvalue())
    
        print(f"ファイルダウンロード：{file_path}")
        
    except HttpError as error:
        print(f"エラー発生：{error}")
        file = None
    
    return None
            
def download_file(real_file_id, name):
    try:
        creds = authenticate()
        service = build('drive', 'v3', credentials=creds)

        destination = os.path.expanduser("~/yasu_device/temp")
        file_path = os.path.join(destination, name)

        request = service.files().get_media(fileId=real_file_id)
        
        # 直接ファイルに書き込む
        with open(file_path, "wb") as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"ダウンロード進行状況: {int(status.progress() * 100)}%")
        
        print(f"ファイルダウンロード：{file_path}")
        
    except HttpError as error:
        print(f"エラー発生：{error}")
    
    return None



if __name__ == '__main__':
    
    folder_id = '1ITNOcJ2xVvw2Bb40qBzd_egp0vpmX8H0'
    files = get_folder_files(folder_id)
    for file in files:
        print(file['id'], file['name'])
        
    for file in files:
        download_file(file['id'], file['name'])
