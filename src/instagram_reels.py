import time
import requests
from config import IG_USER_ID, IG_ACCESS_TOKEN

GRAPH = "https://graph.facebook.com/v19.0"

def _require_ig():
    if not IG_USER_ID or not IG_ACCESS_TOKEN:
        raise RuntimeError("Missing IG_USER_ID or IG_ACCESS_TOKEN")

def publish_reel(video_url: str, caption: str) -> dict:
    """
    IG Reels flow (Graph API):
    1) create media container
    2) poll container status
    3) publish
    """
    _require_ig()

    # 1) create container
    create_url = f"{GRAPH}/{IG_USER_ID}/media"
    payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "access_token": IG_ACCESS_TOKEN,
    }
    r = requests.post(create_url, data=payload, timeout=60)
    r.raise_for_status()
    creation_id = r.json().get("id")
    if not creation_id:
        raise RuntimeError(f"IG create container failed: {r.text}")

    # 2) poll status
    status_url = f"{GRAPH}/{creation_id}"
    for _ in range(90):  # ~ 90 * 5s = 7.5 dk
        rr = requests.get(status_url, params={"fields": "status_code", "access_token": IG_ACCESS_TOKEN}, timeout=30)
        rr.raise_for_status()
        status = rr.json().get("status_code")
        if status == "FINISHED":
            break
        if status in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"IG container status: {status} | {rr.text}")
        time.sleep(5)
    else:
        raise RuntimeError("IG container not finished in time")

    # 3) publish
    publish_url = f"{GRAPH}/{IG_USER_ID}/media_publish"
    pr = requests.post(publish_url, data={"creation_id": creation_id, "access_token": IG_ACCESS_TOKEN}, timeout=60)
    pr.raise_for_status()

    return {"creation_id": creation_id, "publish": pr.json()}
