import shutil
import uuid
from pathlib import Path

from deep_core.aws_links import upload_and_make_link
from deep_core.media_grabber import download_video
from deep_core.settings_box import settings


async def handle_video_request(video_url: str) -> dict:
    job_id = str(uuid.uuid4())
    job_folder: Path = settings.TEMP_FOLDER / job_id

    try:
        video_file, title = await download_video(video_url, job_folder)
        temporary_link = await upload_and_make_link(video_file, job_id)

        return {
            "title": title,
            "file_name": video_file.name,
            "temporary_link": temporary_link,
            "expires_seconds": settings.LINK_EXPIRES_SECONDS,
        }

    finally:
        if job_folder.exists():
            shutil.rmtree(job_folder, ignore_errors=True)