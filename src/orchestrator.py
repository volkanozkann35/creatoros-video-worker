import os
from pathlib import Path

# === LOCAL MODULES ===
from src.vps_uploader import upload_to_vps
from src.instagram_reels import post_reel
from src.caption import reel_caption


def handle_video(video_path: str):
    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(f"Video bulunamadı: {video_path}")

    print(f"🎞 Processing: {video_path}")

    # 1️⃣ VPS'ye upload (STATIC, PRODUCTION SAFE)
    url = upload_to_vps(str(video_path))
    print(f"🌍 Public video URL: {url}")

    # 2️⃣ Instagram Reel gönder
    print("📤 Instagram Reel gönderiliyor...")
    result = post_reel(url, reel_caption())

    print("✅ Instagram Reel yayınlandı")
    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("❌ Kullanım: python orchestrator.py <video_path>")
        sys.exit(1)

    handle_video(sys.argv[1])
