from __future__ import print_function

import pandas as pd
import io
import os.path
import csv
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

csv_file = r"C:\Users\sneha\Desktop\All\PulseLabs\BWS - Week 1.csv"
df = pd.read_csv(csv_file)
#df = df.head(10)

def get_document_ids_from_csv(file_path):
    """Reads the CSV file and returns a list of document IDs from the third column."""
    document_ids = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row == 'Document_ID':
                pass
            if len(row) >= 3:
                document_id = row[2]  
                if document_id:
                    document_ids.append(document_id)
    return document_ids


# The ID of a sample document.
#document_id = '1HQb26fGDBQe1K1bpoBydGiUke0gvO048D978ack17YU'

def download_document(creds, document_id):
    try:
        service = build('docs', 'v1', credentials=creds)

        # Retrieve the document's contents from the Docs service.
        document = service.documents().get(documentId=document_id).execute()

        doc_title = document.get('title')

        # Get the content of the document and save it to a local file.
        content = document.get('body').get('content')
        file_text = ''
        for paragraph in content:
            if 'paragraph' in paragraph:
                elements = paragraph['paragraph']['elements']
                for element in elements:
                    text_run = element['textRun']
                    file_text += text_run['content']

        # Save the content to a local file
        with io.open(f'{doc_title}.txt', 'w', encoding='utf-8') as file:
            file.write(file_text)

        print(f'The content of the document has been downloaded and saved to {doc_title}.txt')
    
    except HttpError as err:
        if err.resp.status == 500:
            print(f"Received HTTP 500 error for document {document_id}. Retrying...")
            # Add a small delay before retrying the request
            time.sleep(10)
            download_document(creds, document_id)  # Retry the request

        else:
            print(f"Error downloading document {document_id}: {err}")
        

def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    try:
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(r'C:\Users\sneha\Desktop\All\PulseLabs\credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        document_ids = get_document_ids_from_csv(csv_file)

        for document_id in document_ids:
            download_document(creds,document_id)
    except HttpError as err:
        print(err)

    '''
    try:
        service = build('docs', 'v1', credentials=creds)

        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=DOCUMENT_ID).execute()

        print('The title of the document is: {}'.format(document.get('title')))
    except HttpError as err:
        print(err)
    '''    

if __name__ == '__main__':
    main()