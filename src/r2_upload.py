from __future__ import annotations
from pathlib import Path
import mimetypes
import boto3
from botocore.config import Config
from config import (
    R2_ACCOUNT_ID, R2_ACCESS_KEY, R2_SECRET_KEY, R2_BUCKET,
    R2_PRESIGN_EXPIRES, R2_PUBLIC_BASE_URL
)

def _require_r2():
    missing = [k for k, v in {
        "R2_ACCOUNT_ID": R2_ACCOUNT_ID,
        "R2_ACCESS_KEY": R2_ACCESS_KEY,
        "R2_SECRET_KEY": R2_SECRET_KEY,
        "R2_BUCKET": R2_BUCKET,
    }.items() if not v]
    if missing:
        raise RuntimeError(f"Missing R2 env vars: {', '.join(missing)}")

def _client():
    _require_r2()
    endpoint = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )

def upload_video_to_r2(local_path: Path, key_prefix: str = "videos") -> dict:
    """
    Upload eder, sonra IG/YouTube kullanabilsin diye:
    - Eğer R2_PUBLIC_BASE_URL verilmişse public URL döner
    - Yoksa presigned URL döner (varsayılan 7 gün)
    """
    local_path = Path(local_path)
    if not local_path.exists():
        raise FileNotFoundError(str(local_path))

    content_type, _ = mimetypes.guess_type(str(local_path))
    content_type = content_type or "video/mp4"

    key = f"{key_prefix}/{local_path.name}"

    s3 = _client()
    s3.upload_file(
        Filename=str(local_path),
        Bucket=R2_BUCKET,
        Key=key,
        ExtraArgs={"ContentType": content_type},
    )

    if R2_PUBLIC_BASE_URL:
        public_url = f"{R2_PUBLIC_BASE_URL.rstrip('/')}/{key}"
        return {"bucket": R2_BUCKET, "key": key, "url": public_url, "mode": "public_base"}
    else:
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": R2_BUCKET, "Key": key},
            ExpiresIn=R2_PRESIGN_EXPIRES,
        )
        return {"bucket": R2_BUCKET, "key": key, "url": url, "mode": "presigned"}
