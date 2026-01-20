import os
from pathlib import Path

def _repo_root() -> Path:
    # /opt/render/project/src/src/config.py -> repo root = /opt/render/project/src
    return Path(__file__).resolve().parent.parent

REPO_ROOT = _repo_root()

def _resolve_path(p: str | None, default: Path) -> Path:
    if not p:
        return default
    path = Path(p)
    if path.is_absolute():
        return path
    # relative -> repo root'a göre çöz
    return (REPO_ROOT / path).resolve()

# --- Watch folder ---
WATCH_FOLDER = _resolve_path(
    os.getenv("WATCH_FOLDER"),
    default=(REPO_ROOT / "auto_videos")
)

# --- Local folders ---
PROCESSED_DIR = _resolve_path(os.getenv("PROCESSED_DIR"), default=(REPO_ROOT / "processed"))
FAILED_DIR = _resolve_path(os.getenv("FAILED_DIR"), default=(REPO_ROOT / "failed"))
LOGS_DIR = _resolve_path(os.getenv("LOGS_DIR"), default=(REPO_ROOT / "logs"))
STATE_DIR = _resolve_path(os.getenv("STATE_DIR"), default=(REPO_ROOT / "state"))

# --- R2 ---
R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID", "").strip()
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY", "").strip()
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY", "").strip()
R2_BUCKET = os.getenv("R2_BUCKET", "").strip()

# Optional: presigned URL expire (seconds)
R2_PRESIGN_EXPIRES = int(os.getenv("R2_PRESIGN_EXPIRES", "604800"))  # 7 days

# Optional: if bucket public, you can set a base URL and skip presign
R2_PUBLIC_BASE_URL = os.getenv("R2_PUBLIC_BASE_URL", "").strip()  # e.g. https://cdn.domain.com

# --- Instagram ---
IG_USER_ID = os.getenv("IG_USER_ID", "").strip()
IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN", "").strip()

# --- YouTube ---
YT_TITLE_PREFIX = os.getenv("YT_TITLE_PREFIX", "SolaraMade").strip()
YT_PRIVACY_STATUS = os.getenv("YT_PRIVACY_STATUS", "public").strip()  # public|unlisted|private
YT_CATEGORY_ID = os.getenv("YT_CATEGORY_ID", "22").strip()  # 22=People & Blogs commonly used

YT_TOKEN_FILE = os.getenv("YT_TOKEN_FILE", "/etc/secrets/youtube_token.json").strip()
YT_CLIENT_FILE = os.getenv("YT_CLIENT_FILE", "/etc/secrets/youtube_client.json").strip()

YT_TOKEN_JSON = os.getenv("YT_TOKEN_JSON", "").strip()
YT_CLIENT_SECRET_JSON = os.getenv("YT_CLIENT_SECRET_JSON", "").strip()

# --- General ---
MIN_FILE_SIZE_BYTES = int(os.getenv("MIN_FILE_SIZE_BYTES", "1024"))  # 1KB: touch ile 0 byte’ı yakalama
POLL_GRACE_SECONDS = int(os.getenv("POLL_GRACE_SECONDS", "3"))  # yazma bitmeden yakalanmasın
