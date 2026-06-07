import argparse
import logging
import re
import smtplib
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, Tag
from xhtml2pdf import pisa

from config import load_email_config
from email_delivery import send_to_kindle
from epub_converter import save_as_epub

logging.getLogger("xhtml2pdf").setLevel(logging.ERROR)


def sanitize_filename(name):
    """Sanitize a string for use as a filename: remove special chars, replace spaces with underscores."""
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"\s+", "_", name).strip("_")
    return name


def fetch_substack_content(url, remove_images=False, font_size="big", medium=False):
    """
    Fetches and parses the post content from either Substack or Medium.

    Returns:
        tuple: The title of the post and the HTML content to convert.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Unable to fetch the page. Status code: {response.status_code}")
        return None, None

    soup = BeautifulSoup(response.text, "html.parser")

    if medium:
        content_div = soup.find("article")
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "Untitled"
        subtitle = ""
    else:
        title_tag = soup.find("h1", class_="post-title")
        if not title_tag:
            title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "Untitled"

        subtitle_tag = soup.find("h3", class_="subtitle")
        subtitle = subtitle_tag.get_text(strip=True) if subtitle_tag else ""

        content_div = soup.find("div", {"class": "body"})

    if not content_div:
        print("Error: Unable to locate the article content. The page structure may have changed.")
        return title, None

    if remove_images:
        for img in content_div.find_all("img"):
            img.decompose()

    for widget in content_div.find_all("div", class_="subscription-widget-wrap"):
        widget.decompose()

    for form in content_div.find_all("form"):
        form.decompose()

    for btn in content_div.find_all("button"):
        btn.decompose()

    for svg in content_div.find_all("svg"):
        svg.decompose()

    for el in content_div.find_all(class_="header-anchor-parent"):
        el.decompose()

    for picture in content_div.find_all("picture"):
        img = picture.find("img")
        if img:
            picture.replace_with(img)
        else:
            picture.decompose()

    for a_tag in content_div.find_all("a", class_="image-link"):
        a_tag.unwrap()

    for inset in content_div.find_all("div", class_="image2-inset"):
        for child in list(inset.children):
            if isinstance(child, Tag) and child.name != "img":
                child.decompose()
        inset.unwrap()

    for tag in content_div.find_all(True):
        if tag.has_attr("style"):
            del tag["style"]

    for img in content_div.find_all("img"):
        if not img.get("src"):
            if src := img.get("data-src"):
                img["src"] = src
            elif srcset := img.get("data-srcset"):
                img["src"] = str(srcset).split(",")[0].split()[0]
            elif orig := img.get("data-original"):
                img["src"] = orig

    if font_size == "small":
        body_font = "18px"
        h1_font = "24px"
        subtitle_font = "18px"
    else:
        body_font = "26px"
        h1_font = "34px"
        subtitle_font = "22px"

    subtitle_html = f"<h3 class='subtitle'>{subtitle}</h3>" if subtitle else ""

    content_html = (
        f"<html dir='ltr'><head><meta charset='utf-8'>"
        f"<style>"
        f"  body {{ font-size: {body_font} !important; line-height: 2.0; margin: 20px; }} "
        f"  h1 {{ font-size: {h1_font} !important; margin-bottom: 10px; }} "
        f"  .subtitle {{ font-size: {subtitle_font} !important; font-weight: normal; "
        f"    color: #555; margin-bottom: 20px; }} "
        f"  p {{ margin-bottom: 15px; }} "
        f"  figure {{ text-align: center; margin: 20px 0; page-break-inside: avoid; }} "
        f"  img {{ max-width: 100%; height: auto; display: block; margin: 10px auto; }} "
        f"  .image-caption, figcaption {{ font-size: 0.8em; color: #666; "
        f"    text-align: center; margin-top: 6px; }} "
        f"  pre, code {{ font-size: 0.85em; background: #f5f5f5; padding: 2px 4px; "
        f"    border-radius: 3px; overflow-x: auto; }} "
        f"  pre {{ padding: 12px; page-break-inside: avoid; }} "
        f"</style>"
        f"</head>"
        f"<body><h1>{title}</h1>\n"
        f"{subtitle_html}\n"
        f"{str(content_div)}</body></html>"
    )
    return title, content_html


def save_as_pdf(content_html, output_filename):
    """Convert the provided HTML to a PDF file."""
    with open(output_filename, "wb") as output_file:
        result = pisa.CreatePDF(content_html, dest=output_file, encoding="utf-8")

    if result.err:
        print(f"Error: PDF generation failed with {result.err} error(s).")
        return False

    print(f"✅ PDF saved as: {output_filename}")
    return True


def _default_output_path(url, title, extension):
    if extension not in {".pdf", ".epub"}:
        raise ValueError(f"Unsupported extension: {extension}")

    slug = urlparse(url).path.rstrip("/").split("/")[-1]
    base_name = slug if slug else sanitize_filename(title)
    return f"{base_name}{extension}"


def _resolve_output_path(requested_output, url, title, extension):
    if requested_output:
        path = requested_output
        if "." not in path.split("/")[-1]:
            path = f"{path}{extension}"
        return path
    return _default_output_path(url, title, extension)


def main():
    parser = argparse.ArgumentParser(
        description="Convert a Substack/Medium post to PDF or EPUB, optionally sending to Kindle."
    )
    parser.add_argument("url", help="URL of the post (Substack or Medium)")
    parser.add_argument(
        "-o",
        "--output",
        help="Output filename or path without extension (extension is added automatically)",
    )
    parser.add_argument(
        "--format",
        choices=["pdf", "epub", "both"],
        default="pdf",
        help="Output format (default: pdf)",
    )
    parser.add_argument("--no-images", action="store_true", help="Exclude images from the output")
    parser.add_argument(
        "--font-size",
        choices=["small", "big"],
        default="big",
        help="Select font size (small or big)",
    )
    parser.add_argument(
        "--medium",
        action="store_true",
        help="Enable Medium article extraction instead of Substack",
    )
    parser.add_argument(
        "--send-email",
        action="store_true",
        help="Email the generated EPUB to your Kindle address (requires SMTP config)",
    )
    parser.add_argument(
        "--email-to",
        help="Override the Kindle destination address for this run",
    )

    args = parser.parse_args()

    if args.send_email and args.format == "pdf":
        print("Note: --send-email requires EPUB output; switching format to epub.")
        args.format = "epub"

    title, content_html = fetch_substack_content(
        url=args.url,
        remove_images=args.no_images,
        font_size=args.font_size,
        medium=args.medium,
    )
    if not content_html:
        print("Failed to retrieve or parse the post content.")
        return

    generated_files = []

    if args.format in ("pdf", "both"):
        pdf_path = _resolve_output_path(args.output, args.url, title, ".pdf")
        if save_as_pdf(content_html, pdf_path):
            generated_files.append(pdf_path)

    if args.format in ("epub", "both"):
        epub_path = _resolve_output_path(args.output, args.url, title, ".epub")
        save_as_epub(title, content_html, epub_path)
        generated_files.append(epub_path)

    if args.send_email:
        epub_candidates = [path for path in generated_files if path.endswith(".epub")]
        if not epub_candidates:
            print("Error: no EPUB was generated to email.")
            return

        try:
            email_config = load_email_config()
            send_to_kindle(
                file_path=epub_candidates[-1],
                subject=title,
                config=email_config,
                recipient=args.email_to,
            )
        except ValueError as exc:
            print(f"Error: {exc}")
        except smtplib.SMTPException as exc:
            print(
                f"Error: SMTP delivery failed: {exc}\n"
                "Make sure your sender email is approved in your Amazon account "
                "and that your SMTP credentials are correct."
            )


if __name__ == "__main__":
    main()
