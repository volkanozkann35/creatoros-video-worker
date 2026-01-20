from __future__ import annotations
import shutil
import time
from pathlib import Path

from logger import setup_logger
from config import PROCESSED_DIR, FAILED_DIR, STATE_DIR, MIN_FILE_SIZE_BYTES, POLL_GRACE_SECONDS
from captions_ai import generate_caption
from r2_upload import upload_video_to_r2
from instagram_reels import publish_reel
from youtube_shorts import upload_short

log = setup_logger("orchestrator")

def _ensure_dirs():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    FAILED_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)

def _wait_until_stable(file_path: Path):
    """
    Dosya yazımı bitmeden yakalanırsa upload bozulur.
    Boyut stabil olana kadar kısa bekleme.
    """
    last = -1
    for _ in range(10):
        if not file_path.exists():
            return
        size = file_path.stat().st_size
        if size == last:
            return
        last = size
        time.sleep(POLL_GRACE_SECONDS)

def process_video(file_path: Path) -> None:
    _ensure_dirs()
    file_path = Path(file_path)

    if not file_path.exists():
        return

    _wait_until_stable(file_path)

    size = file_path.stat().st_size
    if size < MIN_FILE_SIZE_BYTES:
        log.info(f"SKIP (too small): {file_path} size={size}")
        return

    log.info(f"🎬 PROCESS START: {file_path}")

    try:
        meta = generate_caption(file_path)
        title = meta["title"]
        caption = meta["caption"]
        desc = meta["description"]
        tags = meta["tags"]

        # 1) Upload to R2 -> get URL
        up = upload_video_to_r2(file_path, key_prefix="auto_videos")
        video_url = up["url"]
        log.info(f"☁️ R2 OK ({up['mode']}): {video_url}")

        # 2) Instagram Reels
        ig = publish_reel(video_url=video_url, caption=caption)
        log.info(f"📱 IG OK: {ig}")

        # 3) YouTube Shorts
        yt = upload_short(video_path=file_path, title=title, description=desc, tags=tags)
        log.info(f"▶️ YT OK: {yt}")

        # move to processed
        target = PROCESSED_DIR / file_path.name
        shutil.move(str(file_path), str(target))
        log.info(f"✅ DONE -> {target}")

    except Exception as e:
        log.exception(f"❌ FAILED: {file_path} | {e}")
        try:
            target = FAILED_DIR / file_path.name
            if file_path.exists():
                shutil.move(str(file_path), str(target))
            log.info(f"➡️ moved to failed: {target}")
        except Exception:
            log.exception("Failed to move into failed/")
