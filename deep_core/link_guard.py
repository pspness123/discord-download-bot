import re

URL_PATTERN = re.compile(r"https?://[^\s]+")


def find_first_link(text: str) -> str | None:
    result = URL_PATTERN.search(text)

    if result is None:
        return None

    return result.group(0)


def is_valid_web_link(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")