import argparse
import os
import re
import requests
from bs4 import BeautifulSoup
import pdfkit


def sanitize_filename(name):
    """Sanitize a string for use as a filename: remove special chars, replace spaces with underscores."""
    # Remove characters that are not alphanumeric, spaces, hyphens, or underscores
    name = re.sub(r'[^\w\s-]', '', name)
    # Replace whitespace with underscores
    name = re.sub(r'\s+', '_', name).strip('_')
    return name

def fetch_substack_content(url, remove_images=False, font_size='big', medium=False):
    """
    Fetches and parses the post content from either Substack or Medium.
    
    Parameters:
        url (str): The URL of the post.
        remove_images (bool): If True, remove all image tags from the content.
        font_size (str): 'small' or 'big' to adjust the CSS font sizes.
        medium (bool): If True, use Medium-specific selectors for extraction.
    
    Returns:
        tuple: The title of the post and the HTML content to convert.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Unable to fetch the page. Status code: {response.status_code}")
        return None, None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    if medium:
        # For Medium articles, assume the main content is inside an <article> tag.
        content_div = soup.find('article')
        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else "Untitled"
        subtitle = ""
    else:
        # For Substack, find the post title (h1 with class 'post-title') rather
        # than the first h1 which is typically the publication name.
        title_tag = soup.find('h1', class_='post-title')
        if not title_tag:
            title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else "Untitled"

        # Extract the subtitle (h3 with class 'subtitle'), which lives outside
        # the body div.
        subtitle_tag = soup.find('h3', class_='subtitle')
        subtitle = subtitle_tag.get_text(strip=True) if subtitle_tag else ""

        content_div = soup.find('div', {'class': 'body'})
    
    if not content_div:
        print("Error: Unable to locate the article content. The page structure may have changed.")
        return title, None
    
    # Optionally remove images.
    if remove_images:
        for img in content_div.find_all('img'):
            img.decompose()
    
    # --- Clean up unwanted interactive / non-content elements ---

    # Remove subscription widgets ("Type your email…", "Subscribe" CTAs).
    for widget in content_div.find_all('div', class_='subscription-widget-wrap'):
        widget.decompose()

    # Remove all <form> elements (email signup forms).
    for form in content_div.find_all('form'):
        form.decompose()

    # Remove all <button> elements (restack, view-image, etc.).
    for btn in content_div.find_all('button'):
        btn.decompose()

    # Remove all SVG icons (restack arrows, expand icons, etc.).
    for svg in content_div.find_all('svg'):
        svg.decompose()

    # Remove header-anchor interactive overlays on headings.
    for el in content_div.find_all(class_='header-anchor-parent'):
        el.decompose()

    # Simplify <picture> elements: keep only the <img>, drop <source> tags
    # (wkhtmltopdf doesn't support <picture>/<source>).
    for picture in content_div.find_all('picture'):
        img = picture.find('img')
        if img:
            picture.replace_with(img)
        else:
            picture.decompose()

    # Unwrap image link wrappers — replace <a class="image-link ..."> with its
    # children so images aren't wrapped in broken links in the PDF.
    for a_tag in content_div.find_all('a', class_='image-link'):
        a_tag.unwrap()

    # Unwrap the "image2-inset" overlay divs (keep their img children, remove
    # any leftover non-image children like overlay divs).
    for inset in content_div.find_all('div', class_='image2-inset'):
        # Remove non-image children (overlay buttons, divs, etc.)
        for child in list(inset.children):
            if hasattr(child, 'name') and child.name and child.name != 'img':
                child.decompose()
        inset.unwrap()

    # Remove inline styles from all elements to ensure consistent styling.
    for tag in content_div.find_all(True):
        if tag.has_attr('style'):
            del tag['style']

    # Ensure images have a proper src attribute by checking multiple attributes.
    for img in content_div.find_all('img'):
        if not img.get('src'):
            if img.get('data-src'):
                img['src'] = img.get('data-src')
            elif img.get('data-srcset'):
                srcset = img.get('data-srcset')
                first_src = srcset.split(',')[0].split()[0]
                img['src'] = first_src
            elif img.get('data-original'):
                img['src'] = img.get('data-original')
    
    # Set CSS font sizes based on the chosen option.
    if font_size == 'small':
        body_font = "18px"
        h1_font = "24px"
        subtitle_font = "18px"
    else:  # Default to 'big'
        body_font = "26px"
        h1_font = "34px"
        subtitle_font = "22px"
    
    # Build the subtitle HTML if available.
    subtitle_html = f"<h3 class='subtitle'>{subtitle}</h3>" if subtitle else ""

    # Build an HTML document with custom CSS for styling.
    content_html = (
        f"<html><head><meta charset='utf-8'>"
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
    """
    Converts the provided HTML to a PDF file.
    
    Parameters:
        content_html (str): HTML content of the post.
        output_filename (str): The filename for the resulting PDF.
    """
    options = {
        'encoding': 'UTF-8',
        'page-size': 'A4',
        'quiet': '',
        'javascript-delay': '5000',  # Wait 2000ms to allow images to load
    }
    
    # Explicitly set the path to the wkhtmltopdf binary.
    # Update '/usr/local/bin/wkhtmltopdf' if your installation path is different.
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    
    try:
        pdfkit.from_string(content_html, output_filename, options=options, configuration=config)
        print(f"✅ PDF saved as: {output_filename}")
    except Exception as e:
        print("Error during PDF generation:", e)

def main():
    parser = argparse.ArgumentParser(
        description="Convert a Substack/Medium post to a PDF with customizable options."
    )
    parser.add_argument("url", help="URL of the post (Substack or Medium)")
    parser.add_argument("-o", "--output", help="Output PDF filename (defaults to current directory)")
    parser.add_argument("--no-images", action="store_true", help="Exclude images from the output")
    parser.add_argument("--font-size", choices=["small", "big"], default="big", help="Select font size (small or big)")
    parser.add_argument("--medium", action="store_true", help="Enable Medium article extraction instead of Substack")
    
    args = parser.parse_args()
    url = args.url
    
    title, content_html = fetch_substack_content(
        url,
        remove_images=args.no_images,
        font_size=args.font_size,
        medium=args.medium
    )
    if content_html:
        if args.output:
            output_filename = args.output
        else:
            # Derive filename from the URL slug (last path segment).
            from urllib.parse import urlparse
            slug = urlparse(url).path.rstrip('/').split('/')[-1]
            output_filename = f"{slug}.pdf" if slug else f"{sanitize_filename(title)}.pdf"
        save_as_pdf(content_html, output_filename)
    else:
        print("Failed to retrieve or parse the post content.")

if __name__ == "__main__":
    main()
