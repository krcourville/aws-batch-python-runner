import argparse
import asyncio
from dataclasses import asdict
import logging
import boto3
from os import environ
from pathlib import Path
from typing import Iterable
import json

import json_log_formatter
import aiohttp

from lib.gutenberg import FeedItem, GutenbergClient

from lib.helpers import run_command
from lib.io_util import download_file, format_filename
from lib.text_util import word_count

json_formatter = json_log_formatter.VerboseJSONFormatter()
root_logger = logging.getLogger()
log_level = environ.get("LOG_LEVEL", "INFO")
root_logger.setLevel(log_level)

console_handler = logging.StreamHandler()
console_handler.setFormatter(json_formatter)
root_logger.addHandler(console_handler)

logging.getLogger("botocore").setLevel(logging.WARNING)

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
    with open(DEFAULT_DATA_PATH.joinpath("analysis.ndjson"), "w") as outfile:
        for file in indir.iterdir():
            stats = word_count(file)
            result = {"title": file.name, **asdict(stats)}
            result_json = json.dumps(result)
            outfile.write(f"{result_json}\n")


async def ingest_books(indir: Path, outdir: Path):
    await download_books(outdir)
    analyze_books(indir)


def s3_upload_test():
    bucket = get_bucket()
    s3 = boto3.resource("s3")
    content = "Hello s3!"
    res = s3.Object(bucket, "test_file.txt").put(Body=content)
    logger.info("s3-upload-response", extra=dict(s3_res=res))


def get_upload_url(path: str):
    bucket = get_bucket()
    s3 = boto3.client("s3")

    url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params=dict(Bucket=bucket, Key=path, ContentType="text/plain"),
    )
    print(url)


def get_bucket():
    bucket = environ.get("UPLOAD_BUCKET")
    if not bucket:
        raise Exception("Env var is not set: UPLOAD_BUCKET")
    return bucket


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

    # ingest-books
    ingest_books_parser = subparsers.add_parser(
        "ingest-books", help="Run book ingestion process"
    )
    ingest_books_parser.add_argument(
        "--indir",
        type=Path,
        help="directory containing books in plain text",
        default=DEFAULT_DATA_PATH.joinpath("books"),
    )
    ingest_books_parser.add_argument(
        "--outdir",
        type=Path,
        help="output directory to download books to",
        default=DEFAULT_DATA_PATH,
    )
    ingest_books_parser.set_defaults(func=ingest_books, run_async=True)

    # s3-upload-test
    s3_upload_test_parser = subparsers.add_parser(
        "s3-upload-test",
        help="Upload a file to the bucket specified via $UPLOAD_BUCKET",
    )
    s3_upload_test_parser.set_defaults(func=s3_upload_test)

    # get-upload-url
    get_upload_url_parser = subparsers.add_parser(
        "get-upload-url",
        help=(
            "Render to stdout a url for upload to $UPLOAD_BUCKET. "
            "Currently, only text/plain content type is supported"
        ),
    )
    get_upload_url_parser.add_argument("path", help="Target s3 bucket key")
    get_upload_url_parser.set_defaults(func=get_upload_url)

    args = parser.parse_args()
    run_command(args)


if __name__ == "__main__":
    main()
