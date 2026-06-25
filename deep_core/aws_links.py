import asyncio
import mimetypes
from pathlib import Path

import boto3
from botocore.config import Config

from deep_core.settings_box import settings


class StorageProblem(Exception):
    pass


def _create_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID.strip(),
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY.strip(),
        region_name=settings.AWS_REGION.strip(),
        config=Config(
            signature_version="s3v4",
            s3={"addressing_style": "virtual"}
        ),
    )


def _upload_sync(local_file: Path, s3_key: str) -> str:
    if not settings.S3_BUCKET:
        raise StorageProblem("S3_BUCKET is missing in the .env file.")

    content_type, _ = mimetypes.guess_type(local_file.name)

    extra_args = {}

    if content_type:
        extra_args["ContentType"] = content_type

    s3 = _create_s3_client()

    s3.upload_file(
        Filename=str(local_file),
        Bucket=settings.S3_BUCKET,
        Key=s3_key,
        ExtraArgs=extra_args,
    )

    temporary_link = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": settings.S3_BUCKET,
            "Key": s3_key,
        },
        ExpiresIn=settings.LINK_EXPIRES_SECONDS,
    )

    return temporary_link


async def upload_and_make_link(local_file: Path, job_id: str) -> str:
    clean_name = local_file.name.replace(" ", "_")
    s3_key = f"{settings.S3_PREFIX}/{job_id}/{clean_name}"

    return await asyncio.to_thread(_upload_sync, local_file, s3_key)