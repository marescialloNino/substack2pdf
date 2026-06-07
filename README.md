# Substack to PDF / EPUB Converter CLI Tool

## Overview

This command-line tool converts a Substack or Medium post into a **PDF** or **EPUB** file. It fetches the post content, applies custom CSS for styling, and can optionally email the EPUB directly to your Kindle.

## Features

- **PDF and EPUB output** — choose `--format pdf`, `--format epub`, or `--format both`
- **Kindle delivery** — email the EPUB to your Kindle address with `--send-email`
- **Image exclusion** — optionally remove all images with `--no-images`
- **Font customization** — choose `small` or `big` font presets
- **Flexible output paths** — save with a custom filename or location

## Requirements

- Python 3.10+
- Python packages: `requests`, `beautifulsoup4`, `xhtml2pdf`, `ebooklib`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   # venv\Scripts\activate    # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### PDF (default)

```bash
python3 substack2pdf.py "https://cryptohayes.substack.com/p/the-cure"
python3 substack2pdf.py "https://cryptohayes.substack.com/p/pvp" -o ~/Desktop/arthur_hayes_pvp
python3 substack2pdf.py "https://cryptohayes.substack.com/p/the-cure" --font-size small -o ~/Desktop/the_cure
python3 substack2pdf.py "https://cryptohayes.substack.com/p/zero-knowledge-proof" --no-images -o ~/Desktop/zero-knowledge-proof
```

### EPUB

```bash
python3 substack2pdf.py "https://cryptohayes.substack.com/p/the-cure" --format epub
python3 substack2pdf.py "https://cryptohayes.substack.com/p/the-cure" --format epub -o ~/Desktop/the_cure
```

### PDF + EPUB

```bash
python3 substack2pdf.py "https://cryptohayes.substack.com/p/the-cure" --format both
```

### Medium articles

```bash
python3 substack2pdf.py "https://ehandbook.com/teach-me-daddy-33e7a66dfe76" --medium --no-images --font-size small
```

### Send to Kindle

```bash
python3 substack2pdf.py "https://cryptohayes.substack.com/p/the-cure" --format epub --send-email
python3 substack2pdf.py "https://cryptohayes.substack.com/p/the-cure" --send-email --email-to someone@kindle.com
```

`--send-email` generates an EPUB (if needed) and emails it to your Kindle address.

---

## Kindle email setup

### Recommended: use a dedicated sender account

Yes — storing a password locally (config file **or** env vars) is a real risk. Nothing is perfectly safe on disk or in your shell, but you can **limit the blast radius**:

1. Create a **throwaway Gmail account** used only for Kindle delivery, e.g. `your-name.kindlesender@gmail.com`
2. Enable 2FA on that account and create a [Gmail app password](https://myaccount.google.com/apppasswords) for it
3. Add **that address** (not your main inbox) to Amazon's approved sender list
4. Put only those credentials in `~/.config/substack2pdf/config.ini`

If the password leaks, an attacker can at most send EPUBs to your Kindle from that one approved address. They do **not** get access to your real email, contacts, or other accounts.

The dedicated account does not need to receive mail — it only sends.

### What email does the script use?

**An SMTP account you configure** — typically the dedicated sender above. The script connects to your provider's SMTP server (e.g. `smtp.gmail.com`) and sends the EPUB **from** `your-name.kindlesender@gmail.com` **to** your Kindle address (e.g. `yourname@kindle.com`).

You fully control:
- which email account sends the message (use a dedicated one)
- where credentials are stored (prefer config file over env vars — see below)
- when sending happens (only when you pass `--send-email`)

### How do you approve the sender?

Amazon only accepts documents from **approved sender addresses**. This prevents random people from pushing books onto your Kindle.

1. Find your Kindle email address:
   - Amazon website → **Account & Lists** → **Content & Devices** → **Preferences** → **Personal Document Settings**
   - Copy your `@kindle.com` address (or `@free.kindle.com` for Wi-Fi delivery)

2. Approve your **dedicated sender** email:
   - In the same **Personal Document Settings** page, scroll to **Approved Personal Document E-mail List**
   - Add the **exact** address from `smtp.user` (e.g. `your-name.kindlesender@gmail.com`)

3. Configure this tool with that same sender address (see below).

If the sender is not approved, Amazon silently drops the email. The script will report a successful SMTP send, but the book won't appear on your Kindle until the sender is whitelisted.

### Is it secure?

| Risk | Mitigation |
|------|------------|
| Password stored on disk | Use a **dedicated sender account** with nothing valuable in it |
| Password in env vars | Env vars can leak via shell history, `ps`, crash logs, and dotfiles — **prefer `config.ini`** for daily use |
| Config file readable by others | Run `chmod 600 ~/.config/substack2pdf/config.ini` after creating it |
| Main email compromised | Never put your primary inbox in `smtp.user` — use `*.kindlesender@gmail.com` |
| Unwanted Kindle uploads | Amazon's allowlist only permits approved senders |
| Accidental sends | Email only runs when you pass `--send-email` |
| Large attachments | Kindle email limit is ~50 MB; use `--no-images` if needed |

**Config file vs env vars:** both store secrets on your machine. For interactive use, the config file is usually safer — it avoids leaving passwords in terminal history or exported shell sessions. Reserve env vars for CI/automation where you inject secrets from a vault.

### Configuration

Copy the example config and edit it:

```bash
mkdir -p ~/.config/substack2pdf
cp config.example.ini ~/.config/substack2pdf/config.ini
chmod 600 ~/.config/substack2pdf/config.ini
```

Example `~/.config/substack2pdf/config.ini`:

```ini
[smtp]
host = smtp.gmail.com
port = 587
user = your-name.kindlesender@gmail.com
password = your-gmail-app-password
use_tls = true

[kindle]
email = yourname@kindle.com
```

### Environment variables (optional)

Environment variables override the config file. Useful for automation; for daily use, prefer the config file above.

| Variable | Description |
|----------|-------------|
| `SUBSTACK2PDF_SMTP_HOST` | SMTP server hostname |
| `SUBSTACK2PDF_SMTP_PORT` | SMTP port (usually `587`) |
| `SUBSTACK2PDF_SMTP_USER` | Dedicated sender address (must be Amazon-approved) |
| `SUBSTACK2PDF_SMTP_PASSWORD` | App password for the dedicated sender |
| `SUBSTACK2PDF_SMTP_USE_TLS` | `true` or `false` (default: `true`) |
| `SUBSTACK2PDF_KINDLE_EMAIL` | Your `@kindle.com` address |

```bash
export SUBSTACK2PDF_SMTP_HOST=smtp.gmail.com
export SUBSTACK2PDF_SMTP_PORT=587
export SUBSTACK2PDF_SMTP_USER=your-name.kindlesender@gmail.com
export SUBSTACK2PDF_SMTP_PASSWORD=your-app-password
export SUBSTACK2PDF_KINDLE_EMAIL=yourname@kindle.com

python3 substack2pdf.py "https://example.substack.com/p/post" --send-email
```
