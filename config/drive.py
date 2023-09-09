from __future__ import print_function

import os.path
import pickle
from mimetypes import MimeTypes
import io
import shutil
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

class DriveAPI:
    global SCOPES

    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self):
        self.creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle','rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                # flow = InstalledAppFlow.from_client_secrets_file(
                #     'credentials.json', SCOPES)
                flow = InstalledAppFlow.from_client_secrets_file(
                    r'C:\Users\HP\Downloads\client_secret_458878593220-uev3eqpmddp1ptavevhp53fb5dfdff1k.apps.googleusercontent.com.json', SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open('token.pickle','wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('drive','v3', credentials=self.creds)

        results = self.service.files().list(
            pageSize=100, fields="files(id, name)").execute()
        items = results.get('files',[])

    def FileUpload(self, image, name):
        mimetype = MimeTypes().guess_type(name)[0]
        file_metadata = {'name':name}

        try:
            file = self.service.files().create(
                body=file_metadata, media_body=image, fields='id').execute()
            print('Uploaded')
        except:
            raise Exception("Cant Upload")

