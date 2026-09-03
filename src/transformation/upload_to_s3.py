import os
import boto3
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path=env_path)

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

BUCKET = os.getenv("AWS_BUCKET_NAME")

def upload_folder(local_folder, s3_prefix):
    for root, _, files in os.walk(local_folder):
        for file in files:
            local_path = os.path.join(root, file)
            s3_key = f"{s3_prefix}/{file}"
            s3.upload_file(local_path, BUCKET, s3_key)
            print(f"Uploaded {file} to s3://{BUCKET}/{s3_key}")

if __name__ == "__main__":
    upload_folder("data/curated", "curated")