import requests
import time
from src.config import (
    IG_ACCESS_TOKEN,
    IG_USER_ID,
    IG_VERSION
)


def post_reel(video_url: str, caption: str):
    print("📤 Instagram Reel gönderiliyor...")

    create_url = f"https://graph.facebook.com/{IG_VERSION}/{IG_USER_ID}/media"

    payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "access_token": IG_ACCESS_TOKEN
    }

    r = requests.post(create_url, data=payload)
    data = r.json()

    if "id" not in data:
        raise RuntimeError(f"IG container oluşturulamadı: {data}")

    creation_id = data["id"]
    print("🕒 Container hazır olması bekleniyor...")

    # Instagram processing bekleme
    for i in range(20):
        status_url = f"https://graph.facebook.com/{IG_VERSION}/{creation_id}?fields=status_code&access_token={IG_ACCESS_TOKEN}"
        status = requests.get(status_url).json()

        if status.get("status_code") == "FINISHED":
            print("✅ Reel hazır")
            break

        time.sleep(3)
    else:
        raise RuntimeError("Instagram video işleyemedi (timeout)")

    publish_url = f"https://graph.facebook.com/{IG_VERSION}/{IG_USER_ID}/media_publish"

    publish_payload = {
        "creation_id": creation_id,
        "access_token": IG_ACCESS_TOKEN
    }

    pub = requests.post(publish_url, data=publish_payload).json()

    if "id" not in pub:
        raise RuntimeError(f"Reel publish başarısız: {pub}")

    print("🚀 Instagram Reel YAYINLANDI:", pub["id"])
    return pub["id"]
