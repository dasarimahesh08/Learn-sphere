from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import tempfile
import os

SCOPES = ['https://www.googleapis.com/auth/drive.file']


from google.auth.transport.requests import Request

def authenticate_google_drive():
    creds = None

    if os.path.exists("token.json"):
        print("Using existing token")
        creds = Credentials(
            token=os.getenv("GOOGLE_ACCESS_TOKEN"),
            refresh_token=os.getenv("GOOGLE_REFRESH_TOKEN"),
            token_uri=os.getenv("GOOGLE_TOKEN_URI"),
            client_id=os.getenv("GOOGLE_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
            scopes=SCOPES
        )
    else:
        print("No token found")

    if not creds or not creds.valid:

        # refresh expired token
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing token")
            creds.refresh(Request())

        with open("token.json", "w") as token:
            token.write(creds.to_json())

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