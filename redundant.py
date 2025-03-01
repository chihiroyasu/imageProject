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
        return []
    else:
        # print('Files:')
        # for file in files:
        #     print(f"Name: {file['name']}, ID: {file['id']}, Type: {file['mimeType']}")
        return files
    

def search_star_file(folder_id, which):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    # フォルダ内のファイル情報を取得
    results = service.files().list(q=f"'{folder_id}' in parents and starred = {which}",
                                   fields="files(id, name)").execute()
    files = results.get('files', [])

    if not files:
        print('No files found.')
        return []
    else:
        return files

            
def download_file(real_file_id, name):
    try:
        creds = authenticate()
        service = build('drive', 'v3', credentials=creds)

        destination = os.path.expanduser("/mnt/nas/redundant")
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


def move_file(file_id, folder_id):
    try:
        creds = authenticate()
        service = build('drive', 'v3', credentials=creds)
        
        file = service.files().get(fileId=file_id, fields="parents").execute()
        previous_parents = ",".join(file.get("parents", []))  # None回避
        
        # file = {
        #     service.files()
        #     .update(
        #         fileId=file_id,
        #         addParents=folder_id,
        #         removeParents=previous_parents,
        #         fields="id, parents",
        #     )
        # }
        # ファイル移動（波括弧 `{}` を削除）
        file = service.files().update(
            fileId=file_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields="id, parents",
        ).execute()  # ここで API を実行し、辞書を返す

        return file.get("parents")  # file は辞書なので .get() を使える

    except HttpError as error:
        print(f"エラー発生：{error}")
        return None
    
def throw_away(file_id):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    body_value = {'trashed': True}
    response = service.files().update(fileId=file_id, body=body_value).execute()
    return response
    




if __name__ == '__main__':
    
    temp_folder_id = '1ITNOcJ2xVvw2Bb40qBzd_egp0vpmX8H0'
    star_folder_id = '1wyFz2o6Q1X0lTjGl1yS2HDuHqcWEj9h_'
    
    files = get_folder_files(temp_folder_id)
    for file in files:
        print(file['id'], file['name'])
    
    print("###### star付き #####")
    star_files = search_star_file(temp_folder_id, "true")
    for file in star_files:
        print(file['id'], file['name'])
        
    print("###### star付いてない #####")
    not_star_files = search_star_file(temp_folder_id, "false")
    for file in not_star_files:
        print(file['id'], file['name'])
        
    for file in files:
        download_file(file['id'], file['name'])
        
    for file in star_files:
        move_file(file['id'], star_folder_id)
        
    for file in not_star_files:
        throw_away(file['id'])
        
    
