import argparse
import os
import requests
from bs4 import BeautifulSoup
import pdfkit

def fetch_substack_content(url, remove_images=False, font_size='big'):
    """
    Fetches and parses the Substack post content.

    Parameters:
        url (str): The URL of the Substack post.
        remove_images (bool): If True, remove all image tags from the content.
        font_size (str): 'small' or 'big' to adjust the CSS font sizes.

    Returns:
        tuple: The title of the post and the HTML content to convert.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Unable to fetch the page. Status code: {response.status_code}")
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Locate the post title (typically in an <h1> tag)
    title_tag = soup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else "Untitled"
    
    # Locate the main content of the post (adjust the selector if needed)
    content_div = soup.find('div', {'class': 'body'})
    if not content_div:
        print("Error: Unable to locate the article content. The page structure may have changed.")
        return title, None

    # Optionally remove images from the content
    if remove_images:
        for img in content_div.find_all('img'):
            img.decompose()

    # Set CSS font sizes based on the chosen option
    if font_size == 'small':
        body_font = "14px"
        h1_font = "22px"
    else:  # Default to 'big'
        body_font = "18px"
        h1_font = "28px"

    # Build an HTML document with custom CSS for styling.
    content_html = (
        f"<html><head><meta charset='utf-8'>"
        f"<style>"
        f"  body {{ font-size: {body_font}; line-height: 2.0; margin: 20px; }} "
        f"  h1 {{ font-size: {h1_font}; margin-bottom: 20px; }} "
        f"  p {{ margin-bottom: 15px; }} "
        f"</style>"
        f"</head>"
        f"<body><h1>{title}</h1>\n"
        f"{str(content_div)}</body></html>"
    )
    return title, content_html

def save_as_pdf(content_html, output_filename):
    """
    Converts the provided HTML to a PDF file.

    Parameters:
        content_html (str): HTML content of the Substack post.
        output_filename (str): The filename for the resulting PDF.
    """
    options = {
        'encoding': 'UTF-8',
        'page-size': 'A4',
        'quiet': ''
    }
    
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    
    try:
        pdfkit.from_string(content_html, output_filename, options=options, configuration=config)
        print(f"✅ PDF saved as: {output_filename}")
    except Exception as e:
        print("Error during PDF generation:", e)

def main():
    parser = argparse.ArgumentParser(description="Convert a Substack post to a PDF with customizable options.")
    parser.add_argument("url", help="URL of the Substack post")
    parser.add_argument("-o", "--output", help="Output PDF filename (if not provided, the file will be saved to your Desktop)")
    parser.add_argument("--no-images", action="store_true", help="Exclude images from the output")
    parser.add_argument("--font-size", choices=["small", "big"], default="big", help="Select font size (small or big)")

    args = parser.parse_args()
    url = args.url

    title, content_html = fetch_substack_content(url, remove_images=args.no_images, font_size=args.font_size)
    if content_html:
        if args.output:
            output_filename = args.output
        else:
            # Save to Desktop by default if no output file is provided.
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            output_filename = os.path.join(desktop_path, f"{title}.pdf")
        save_as_pdf(content_html, output_filename)
    else:
        print("Failed to retrieve or parse the post content.")

if __name__ == "__main__":
    main()
