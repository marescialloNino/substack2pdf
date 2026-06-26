# Substack to EPUB / PDF Converter

Convert Substack or Medium posts into **EPUB** or **PDF** files for e-readers, offline reading, or Kindle.

## Features

- **EPUB by default** — Kindle-ready format with embedded images
- **PDF output** — optional via `--format pdf`
- **Substack-optimized extraction** — strips subscribe widgets, buttons, and cruft
- **Font presets** — `small` or `big` (applies to both EPUB and PDF)
- **Image control** — include images by default, or `--no-images` for text-only
- **Medium support** — `--medium` for Medium-hosted articles

## Requirements

- Python 3.10+
- Dependencies: `requests`, `beautifulsoup4`, `ebooklib`, `xhtml2pdf`

No external binaries required. PDF generation uses pure-Python `xhtml2pdf` (not wkhtmltopdf or pdfkit).

## Installation

```bash
git clone <repository-url>
cd substack2pdf

python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

## Usage

### EPUB (default)

```bash
python3 substack2pdf.py "https://cryptohayes.substack.com/p/the-cure"
python3 substack2pdf.py "https://cryptohayes.substack.com/p/the-cure" -o ~/Desktop/the-cure
python3 substack2pdf.py "https://cryptohayes.substack.com/p/the-cure" --font-size small
python3 substack2pdf.py "https://cryptohayes.substack.com/p/the-cure" --no-images
```

Output defaults to `{slug}.epub` in the current directory (e.g. `the-cure.epub`).

### PDF

```bash
python3 substack2pdf.py "https://cryptohayes.substack.com/p/the-cure" --format pdf
python3 substack2pdf.py "https://cryptohayes.substack.com/p/pvp" --format pdf -o ~/Desktop/pvp
```

### Both formats

```bash
python3 substack2pdf.py "https://cryptohayes.substack.com/p/the-cure" --format both
```

### Medium articles

```bash
python3 substack2pdf.py "https://medium.com/..." --medium --no-images --font-size small
```

## Getting the EPUB onto your Kindle

This tool generates the file locally. To read on Kindle:

1. **USB** — Connect your Kindle, enable "Transfer files via USB", copy the `.epub` to the `documents/` folder.
2. **Amazon Send to Kindle** — Upload at [amazon.com/sendtokindle](https://www.amazon.com/sendtokindle) (Amazon login, no SMTP setup).
3. **Kindle app** — Open the EPUB via the Send to Kindle app on desktop or mobile.

## CLI reference

| Flag | Description |
|------|-------------|
| `url` | Substack or Medium post URL (required) |
| `-o`, `--output` | Output path without extension |
| `--format epub\|pdf\|both` | Output format (default: `epub`) |
| `--font-size small\|big` | Font size preset (default: `big`) |
| `--no-images` | Strip all images |
| `--medium` | Use Medium article selectors |

## Project docs

- [COMPETITORS.md](COMPETITORS.md) — landscape of similar tools
- [TODO.md](TODO.md) — planned improvements
