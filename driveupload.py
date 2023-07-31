import os
import io
import argparse
import google.auth
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import tkinter as tk
from tkinter import filedialog


# Create GUI for file selection
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()


# Get file name from path

filename = os.path.basename(file_path)


# Authenticate with Google Drive API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'credentials.json'
creds, project = google.auth.default()
service = build('drive', 'v3', credentials=creds)


# Check if file already exists in Google Drive
try:
    query = "name='{}' and trashed=false".format(filename)
    response = service.files().list(q=query).execute()
    if len(response['files']) > 0:
        print("File with name '{}' already exists in Google Drive".format(filename))
        exit()
except HttpError as error:
    print("An error occurred while checking if file exists: {}".format(error))
    exit()


# Upload file to Google Drive
try:
    file_metadata = {'name': filename}
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print("File ID: {}".format(file.get('id')))
except HttpError as error:
    print("An error occurred while uploading file: {}".format(error))
    exit()
