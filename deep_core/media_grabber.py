import asyncio
from pathlib import Path
from typing import Any

import yt_dlp

from deep_core.settings_box import settings


class DownloadProblem(Exception):
    pass


def _download_sync(video_url: str, target_folder: Path) -> tuple[Path, str]:
    target_folder.mkdir(parents=True, exist_ok=True)

    max_size = settings.MAX_FILE_SIZE_MB

    ydl_options: dict[str, Any] = {
        "format": (
            f"best[ext=mp4][filesize<{max_size}M]"
            f"/best[ext=mp4]"
            f"/best[filesize<{max_size}M]"
            "/best"
        ),
        "outtmpl": str(target_folder / "%(title).80s_%(id)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "restrictfilenames": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(video_url, download=True)

    except Exception as error:
        raise DownloadProblem(f"yt-dlp could not download this link: {error}") from error

    downloaded_files = [
        file
        for file in target_folder.iterdir()
        if file.is_file()
        and not file.name.endswith(".part")
        and not file.name.endswith(".ytdl")
    ]

    if not downloaded_files:
        raise DownloadProblem("Download finished, but no video file was found.")

    video_file = max(downloaded_files, key=lambda file: file.stat().st_mtime)

    size_mb = video_file.stat().st_size / 1024 / 1024

    if size_mb > settings.MAX_FILE_SIZE_MB:
        raise DownloadProblem(
            f"The downloaded file is too large: {size_mb:.1f} MB"
        )

    title = info.get("title", video_file.stem) if isinstance(info, dict) else video_file.stem

    return video_file, title


async def download_video(video_url: str, target_folder: Path) -> tuple[Path, str]:
    return await asyncio.to_thread(_download_sync, video_url, target_folder)