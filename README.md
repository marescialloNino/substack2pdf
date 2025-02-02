# Substack to PDF Converter CLI Tool

## Overview
This command-line tool converts a Substack post into a PDF file. It fetches the post content, applies custom CSS for styling (such as customizable font sizes), and then generates a PDF using wkhtmltopdf via the pdfkit library.

## Objectives
- **Fetch Content:** Retrieve the HTML content and title from a specified Substack post.
- **Custom Styling:** Apply custom CSS to adjust text sizes, line height, margins, and other formatting details.
- **Optional Image Removal:** Provide an option to exclude images from the PDF.
- **Custom Font Size:** Allow users to choose between small and big font sizes.
- **Flexible Output:** Enable users to save the output PDF with a custom file name and location (e.g., directly to the Desktop).

## Features
- **CLI-Based Operation:** Use command-line arguments to control the conversion process.
- **Image Exclusion:** Optionally remove all images from the post before conversion.
- **Font Customization:** Choose between predefined font size presets (`small` or `big`).
- **Custom Titles:** Optionally override the post's title with a custom title for both the PDF header and file name.
- **Automatic Desktop Saving:** If no output path is specified, the PDF is saved to the user’s Desktop with the post's title as the filename.

## Requirements
- Python packages: `requests`, `beautifulsoup4`, and `pdfkit`
- wkhtmltopdf (Installed and available in the system PATH or specified explicitly in the code)

## Installation

1. Clone the repository:
    - git clone <repository-url>
    - cd <repository-folder>

2. Create a virtual environment(good practice):
    - python -m venv venv
       - source venv/bin/activate  # On macOS/Linux
        - venv\Scripts\activate     # On Windows

3. Install the required Python packages:
    - pip install -r requirements.txt

4. Install wkhtmltopdf:
    - https://wkhtmltopdf.org/downloads.html
    - Add wkhtmltopdf to the system PATH

5. Run the script

## Usage

Export with default settings (big font with images, title taken from post name):
- python3 substack2pdf.py "https://cryptohayes.substack.com/p/the-cure"

Export with custom title:
- python3 substack2pdf.py "https://cryptohayes.substack.com/p/pvp" --output ~/Desktop/arthur_hayes_pvp.pdf


Export with custom title and font:
- python3 substack2pdf.py "https://cryptohayes.substack.com/p/the-cure" --font-size small -o ~/Desktop/arthur_hayes_the_cure.pdf

Export without images and custom title:
- python3 substack2pdf.py "https://cryptohayes.substack.com/p/the-cure" --no-images --o ~/Desktop/no_images.pdf

Export from Medium (Cannot render images for now):
- python3 substack2pdf.py "https://ehandbook.com/teach-me-daddy-33e7a66dfe76" --medium --no-images --font-size small
 
