import os
import re
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import io

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'avito-xml-333413-1834999ce57d.json'

def create_service():
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    return service

service = create_service()

def find_photos(folder_name):
    folder = service.files().list(q=f"'1oRIlW214GlnQSs7QFg_3K6ebYvCBcJkg' in parents and name = '{folder_name}'").execute().get('files')
    if folder:
        folder_id = folder[0].get('id')
        photo_arr = service.files().list(
            q=f"'{folder_id}' in parents"
        ).execute().get('files')

        return photo_arr
    return []

def save_photos(photo_arr, folder_name):
    if photo_arr:
        paths = []
        for i in range(len(photo_arr)):
            request = service.files().get_media(fileId=photo_arr[i].get('id'))
            filename = f'src/{folder_name}/{i+1}.jpeg'
            if os.path.exists(filename):
                print(f'Фото уже есть - {i}')
                paths.append(f"http://89.108.81.163:5000/{filename}")
                continue
            if not os.path.exists(f'src/{folder_name}'):
                os.makedirs(f'src/{folder_name}')
            fh = io.FileIO(filename, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))
            paths.append(f"http://89.108.81.163:5000/{filename}")
        
        return paths
    return []

def main_photos(folder_name):
    return save_photos(find_photos(folder_name), folder_name)

    


if __name__ == "__main__":
    print(main('1'))
    
