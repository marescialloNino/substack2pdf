"""Convert article HTML to EPUB with embedded images."""

import mimetypes
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from ebooklib import epub

USER_AGENT = "Mozilla/5.0"
MAX_IMAGE_BYTES = 10 * 1024 * 1024

FONT_PRESETS = {
    "small": {"body": "18px", "h1": "24px", "subtitle": "18px"},
    "big": {"body": "26px", "h1": "34px", "subtitle": "22px"},
}


def _guess_extension(url: str, content_type: str | None) -> str:
    if content_type:
        ext = mimetypes.guess_extension(content_type.split(";")[0].strip())
        if ext:
            return ext
    path = urlparse(url).path
    suffix = Path(path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}:
        return suffix
    return ".jpg"


def _media_type_for_extension(ext: str) -> str:
    mapping = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
    }
    return mapping.get(ext.lower(), "image/jpeg")


def _build_stylesheet(font_size: str) -> str:
    sizes = FONT_PRESETS.get(font_size, FONT_PRESETS["big"])
    return (
        f"body {{ font-family: serif; font-size: {sizes['body']}; "
        f"line-height: 1.6; margin: 1em; }} "
        f"h1 {{ font-size: {sizes['h1']}; margin-bottom: 0.5em; }} "
        f".subtitle {{ font-size: {sizes['subtitle']}; color: #555; margin-bottom: 1em; }} "
        "p { margin-bottom: 1em; } "
        "figure { text-align: center; margin: 1.5em 0; } "
        "img { max-width: 100%; height: auto; display: block; margin: 0.5em auto; } "
        ".image-caption, figcaption { font-size: 0.85em; color: #666; text-align: center; } "
        "pre, code { font-family: monospace; font-size: 0.9em; background: #f5f5f5; "
        "padding: 0.2em 0.4em; border-radius: 3px; } "
        "pre { padding: 0.8em; overflow-x: auto; white-space: pre-wrap; }"
    )


def _embed_images(body, book: epub.EpubBook, session: requests.Session) -> None:
    for index, img in enumerate(body.find_all("img")):
        src = img.get("src")
        if not src or src.startswith("data:"):
            continue

        try:
            response = session.get(src, timeout=30)
            response.raise_for_status()
            if len(response.content) > MAX_IMAGE_BYTES:
                print(f"Warning: skipping large image ({len(response.content)} bytes): {src}")
                img.decompose()
                continue

            ext = _guess_extension(src, response.headers.get("Content-Type"))
            image_name = f"images/img_{index:03d}{ext}"
            image_item = epub.EpubImage()
            image_item.file_name = image_name
            image_item.content = response.content
            image_item.media_type = _media_type_for_extension(ext)
            book.add_item(image_item)
            img["src"] = image_name
        except requests.RequestException as exc:
            print(f"Warning: could not download image {src}: {exc}")
            img.decompose()


def save_as_epub(
    title: str,
    content_html: str,
    output_filename: str,
    font_size: str = "big",
) -> None:
    """Convert HTML content to an EPUB file with embedded images."""
    book = epub.EpubBook()
    book.set_identifier(output_filename)
    book.set_title(title)
    book.set_language("en")

    soup = BeautifulSoup(content_html, "html.parser")
    body = soup.find("body")
    if body is None:
        raise ValueError("HTML content is missing a <body> element.")

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    _embed_images(body, book, session)

    style = epub.EpubItem(
        uid="style",
        file_name="style/main.css",
        media_type="text/css",
        content=_build_stylesheet(font_size),
    )
    book.add_item(style)

    chapter = epub.EpubHtml(title=title, file_name="chapter.xhtml", lang="en")
    chapter.content = str(body)
    chapter.add_item(style)
    book.add_item(chapter)

    book.toc = (epub.Link("chapter.xhtml", title, "chapter"),)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav", chapter]

    epub.write_epub(output_filename, book)
    print(f"✅ EPUB saved as: {output_filename}")
