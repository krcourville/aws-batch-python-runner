import argparse
import asyncio
from dataclasses import asdict
import logging
import json_log_formatter

from pathlib import Path
from typing import Iterable

import aiohttp
from lib.gutenberg import FeedItem, GutenbergClient

from lib.helpers import run_command
from lib.io_util import download_file, format_filename
from lib.text_util import word_count

json_formatter = json_log_formatter.JSONFormatter()
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(json_formatter)
root_logger.addHandler(console_handler)


logger = logging.getLogger(__file__)

DEFAULT_DATA_PATH = Path("./data/gb-books")


def format_target_path(outdir: Path, name: str) -> Path:
    filename = format_filename(name)
    return outdir.joinpath(f"{filename}.txt")


async def download_book_files(outdir: Path, items: Iterable[FeedItem]):
    books_dir = outdir.joinpath("books")
    books_dir.mkdir(parents=True, exist_ok=True)
    async with aiohttp.ClientSession() as session:
        downloads = [
            download_file(
                session=session,
                url=item.get_text_link(),
                path=format_target_path(outdir=books_dir, name=item.title),
            )
            for item in items
        ]
        await asyncio.gather(*downloads)


async def download_books(outdir: Path):
    async with GutenbergClient() as client:
        feed_file = await client.download_feed(outdir)
        feed_items = client.parse_feed(feed_file)
        await download_book_files(outdir, feed_items)


def analyze_books(indir: Path):
    for file in indir.iterdir():
        text = file.read_text("UTF-8")
        stats = word_count(text)
        result = {"title": file.name, **asdict(stats)}
        logger.info("book-analysis", extra=result)


def main():
    parser = argparse.ArgumentParser(
        description="Utilities for working with data from [Project Gutenberg](https://www.gutenberg.org)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # download-books
    download_parser = subparsers.add_parser(
        "download-books", help="download a sampling of books"
    )
    download_parser.add_argument(
        "--outdir",
        type=Path,
        help="output directory to download books to",
        default=DEFAULT_DATA_PATH,
    )
    download_parser.set_defaults(func=download_books, run_async=True)

    # analyze-books
    analyze_books_parser = subparsers.add_parser(
        "analyze-books", help="Analyze word usage on downloaded books"
    )
    analyze_books_parser.add_argument(
        "--indir",
        type=Path,
        help="directory containing books in plain text",
        default=DEFAULT_DATA_PATH.joinpath("books"),
    )
    analyze_books_parser.set_defaults(func=analyze_books)

    args = parser.parse_args()
    run_command(args)


if __name__ == "__main__":
    main()
