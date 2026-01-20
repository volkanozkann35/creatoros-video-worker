from __future__ import annotations
import json
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from config import (
    YT_TITLE_PREFIX, YT_PRIVACY_STATUS, YT_CATEGORY_ID,
    YT_TOKEN_FILE, YT_CLIENT_FILE, YT_TOKEN_JSON, YT_CLIENT_SECRET_JSON
)

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def _load_json_from_env_or_file(env_json: str, file_path: str) -> dict | None:
    if env_json:
        return json.loads(env_json)
    p = Path(file_path)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return None

def _get_credentials() -> Credentials | None:
    token_data = _load_json_from_env_or_file(YT_TOKEN_JSON, YT_TOKEN_FILE)
    client_data = _load_json_from_env_or_file(YT_CLIENT_SECRET_JSON, YT_CLIENT_FILE)

    if not token_data or not client_data:
        return None

    # token_data: refresh_token vs.
    creds = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri=token_data.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=token_data.get("client_id") or client_data.get("installed", {}).get("client_id") or client_data.get("web", {}).get("client_id"),
        client_secret=token_data.get("client_secret") or client_data.get("installed", {}).get("client_secret") or client_data.get("web", {}).get("client_secret"),
        scopes=token_data.get("scopes") or SCOPES,
    )

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds

def upload_short(video_path: Path, title: str, description: str, tags: list[str]) -> dict:
    creds = _get_credentials()
    if not creds:
        raise RuntimeError("YouTube creds not configured (youtube_token.json + youtube_client.json missing).")

    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": f"{YT_TITLE_PREFIX} - {title}"[:95],
            "description": description,
            "tags": tags[:30],
            "categoryId": YT_CATEGORY_ID,
        },
        "status": {
            "privacyStatus": YT_PRIVACY_STATUS
        }
    }

    media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype="video/mp4")

    req = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    resp = None
    while resp is None:
        status, resp = req.next_chunk()

    return resp
