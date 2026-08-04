from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import tempfile
import os
import re
SCOPES = ['https://www.googleapis.com/auth/drive.file']


from google.auth.transport.requests import Request

def authenticate_google_drive():
    creds = Credentials(
        token=os.getenv("GOOGLE_ACCESS_TOKEN"),
        refresh_token=os.getenv("GOOGLE_REFRESH_TOKEN"),
        token_uri=os.getenv("GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        scopes=SCOPES,
    )

    if not creds.valid:
        if creds.refresh_token:
            print("Refreshing token")
            creds.refresh(Request())
        else:
            raise Exception(
                "No valid Google Drive credentials — check GOOGLE_ACCESS_TOKEN, "
                "GOOGLE_REFRESH_TOKEN, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET env vars on Render."
            )

    service = build("drive", "v3", credentials=creds)
    return service
    
def upload_file_to_drive(uploaded_file):
    service = authenticate_google_drive()

    # create temporary file
    temp = tempfile.NamedTemporaryFile(delete=False)
    for chunk in uploaded_file.chunks():
        temp.write(chunk)

    temp.close()

    file_metadata = {
        "name": uploaded_file.name , 
        "parents": ["1WqJ9x_YsFdzUAce0H7YvkPEmy5XDYMbx"]
    }

    media = MediaFileUpload(
    temp.name,
    mimetype=uploaded_file.content_type,
    resumable=True
    )

    request = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    )

    response = None

    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    service.permissions().create(
        fileId=response.get("id"),
        body={
            "role": "reader",
            "type": "anyone"
        }
    ).execute()
    return response.get("id")

def get_drive_file_url(file_id):
    return f"https://drive.google.com/file/d/{file_id}/preview?usp=sharing"

def extract_file_id(drive_url):
    """
    Extracts the Google Drive file ID from a URL like:
    https://drive.google.com/file/d/1AbCdEfGhIjKlMnOp/preview?usp=sharing
    """
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', drive_url)
    if match:
        return match.group(1)
    return None

def delete_file_from_drive(drive_url):

    service = authenticate_google_drive()
    try:
        service.files().delete(fileId=file_id).execute()
        return True
    except Exception as e:
        print("Drive delete error:", e)
        return False