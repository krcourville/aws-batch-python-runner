import logging
from pathlib import Path
import string

import aiohttp

_logger = logging.getLogger(__name__)

CHUNK_SIZE = 512


async def download_file(session: aiohttp.ClientSession, url: str, path: Path) -> Path:
    async with session.get(url) as res:
        with path.open("wb") as file:
            async for chunk in res.content.iter_chunked(CHUNK_SIZE):
                file.write(chunk)
    _logger.info("download_file:success", extra=dict(url=url, path=path.absolute()))
    return path


def format_filename(s: str) -> str:
    """Take a string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.

    Note: this method may produce invalid filenames such as ``, `.` or `..`
    When I use this method I prepend a date string like '2009_01_15_19_46_32_'
    and append a file extension like '.txt', so I avoid the potential of using
    an invalid filename.

    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = "".join(c for c in s if c in valid_chars)
    filename = filename.replace(" ", "_")  # I don't like spaces in filenames.
    return filename
