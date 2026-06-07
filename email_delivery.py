"""Send generated ebooks to a Kindle address via SMTP."""

import mimetypes
import smtplib
from email.message import EmailMessage
from pathlib import Path

from config import EmailConfig

KINDLE_ATTACHMENT_LIMIT_BYTES = 50 * 1024 * 1024


def send_to_kindle(
    file_path: str,
    subject: str,
    config: EmailConfig,
    recipient: str | None = None,
) -> None:
    """Email an ebook file to a Kindle address using the configured SMTP account."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Attachment not found: {file_path}")

    file_size = path.stat().st_size
    if file_size > KINDLE_ATTACHMENT_LIMIT_BYTES:
        raise ValueError(
            f"Attachment is too large for Kindle email delivery "
            f"({file_size} bytes; limit is {KINDLE_ATTACHMENT_LIMIT_BYTES} bytes). "
            "Try --no-images or save the file locally instead."
        )

    mime_type, _ = mimetypes.guess_type(path.name)
    if mime_type is None:
        mime_type = "application/octet-stream"
    maintype, subtype = mime_type.split("/", 1)

    to_address = recipient or config.kindle_email
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = config.smtp.user
    message["To"] = to_address
    message.set_content(
        "Sent by substack2pdf. The attached ebook should appear on your Kindle shortly."
    )
    message.add_attachment(
        path.read_bytes(),
        maintype=maintype,
        subtype=subtype,
        filename=path.name,
    )

    with smtplib.SMTP(config.smtp.host, config.smtp.port, timeout=60) as server:
        if config.smtp.use_tls:
            server.starttls()
        server.login(config.smtp.user, config.smtp.password)
        server.send_message(message)

    print(f"✅ Emailed {path.name} to {to_address} from {config.smtp.user}")
