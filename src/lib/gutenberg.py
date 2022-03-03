from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET

import logging
from types import TracebackType
from typing import Iterable, Optional, Type
from urllib.parse import urlparse

import aiohttp

from .io_util import download_file

FEED_URL = "https://www.gutenberg.org/cache/epub/feeds/today.rss"


@dataclass
class FeedItem:
    title: str
    link: str

    def get_text_link(self):
        return f"{self.link}.txt.utf-8"


class GutenbergClient(object):
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)
        self._session = aiohttp.ClientSession(raise_for_status=True)

    async def close(self) -> None:
        return await self._session.close()

    async def __aenter__(self) -> "GutenbergClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        await self.close()
        return None

    async def download_feed(self, outdir: Path) -> Path:
        f"""
        Downloads English-only books from the gutenberg project "today" feed
        and returns the resulting file path

        Feed Url: {FEED_URL}

        ## Data Sample

        <?xml version="1.0" encoding="utf-8" ?>
        <rss version="0.91">
        <channel>
            <title>Project Gutenberg Recently Posted or Updated EBooks</title>
            <link>http://www.gutenberg.org</link>
            <description>
                EBooks posted or updated today on Project Gutenberg.
                This feed is regenerated every night.
            </description>
            <language>en-us</language>
            <webMaster>webmaster@gutenberg.org (Marcello Perathoner)</webMaster>
            <pubDate>Tue, 15 Feb 2022 11:51:36 -0500</pubDate>
            <lastBuildDate>Tue, 15 Feb 2022 11:51:36 -0500</lastBuildDate>
            <item>
                <title>The Husbandâ€™s Story by David Graham Phillips</title>
                <link>http://www.gutenberg.org/ebooks/67406</link>
                <description>Language: English</description>
            </item>
        </channel>
        """
        outdir.mkdir(parents=True, exist_ok=True)
        filename = Path(urlparse(FEED_URL).path).name
        feed_filepath = outdir.joinpath(filename)

        await download_file(self._session, FEED_URL, feed_filepath)
        return feed_filepath

    def parse_feed(self, file: Path) -> Iterable[FeedItem]:
        tree = ET.parse(file)
        root = tree.getroot()

        for item in root.findall("./channel/item"):
            yield FeedItem(title=item.find("title").text, link=item.find("link").text)
