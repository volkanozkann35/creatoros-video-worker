import os
import boto3
from botocore.client import Config
from dotenv import load_dotenv

load_dotenv()

R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET = os.getenv("R2_BUCKET")

PUBLIC_DEV_URL = "https://pub-50acb4ee9be541f082d1e97fa529bbda.r2.dev"


def upload_video(file_path: str) -> str:
    filename = os.path.basename(file_path)

    s3 = boto3.client(
        "s3",
        endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )

    s3.upload_file(
        file_path,
        R2_BUCKET,
        filename,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": "video/mp4"
        }
    )

    public_url = f"{PUBLIC_DEV_URL}/{filename}"
    print(f"☁ RAW R2 URL: {public_url}")

    return public_url
