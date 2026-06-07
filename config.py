"""Load SMTP and Kindle settings from environment variables or a local config file."""

import configparser
import os
from dataclasses import dataclass
from pathlib import Path


CONFIG_PATH = Path.home() / ".config" / "substack2pdf" / "config.ini"


@dataclass
class SmtpConfig:
    host: str
    port: int
    user: str
    password: str
    use_tls: bool = True


@dataclass
class EmailConfig:
    smtp: SmtpConfig
    kindle_email: str


def _env(name: str) -> str | None:
    value = os.environ.get(name)
    return value.strip() if value else None


def _parse_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _load_ini() -> configparser.ConfigParser | None:
    if not CONFIG_PATH.exists():
        return None
    parser = configparser.ConfigParser(interpolation=None)
    parser.read(CONFIG_PATH)
    return parser


def load_email_config() -> EmailConfig:
    """
    Load email settings. Environment variables override values from config.ini.

    For security, use a dedicated sender account (e.g. your-name.kindlesender@gmail.com)
    rather than your main inbox. Prefer config.ini over env vars for daily use.

    Environment variables:
        SUBSTACK2PDF_SMTP_HOST
        SUBSTACK2PDF_SMTP_PORT
        SUBSTACK2PDF_SMTP_USER
        SUBSTACK2PDF_SMTP_PASSWORD
        SUBSTACK2PDF_SMTP_USE_TLS
        SUBSTACK2PDF_KINDLE_EMAIL
    """
    ini = _load_ini()
    smtp_section = ini["smtp"] if ini and ini.has_section("smtp") else {}
    kindle_section = ini["kindle"] if ini and ini.has_section("kindle") else {}

    host = _env("SUBSTACK2PDF_SMTP_HOST") or smtp_section.get("host")
    port_raw = _env("SUBSTACK2PDF_SMTP_PORT") or smtp_section.get("port", "587")
    user = _env("SUBSTACK2PDF_SMTP_USER") or smtp_section.get("user")
    password = _env("SUBSTACK2PDF_SMTP_PASSWORD") or smtp_section.get("password")
    use_tls_raw = _env("SUBSTACK2PDF_SMTP_USE_TLS") or smtp_section.get("use_tls", "true")
    kindle_email = _env("SUBSTACK2PDF_KINDLE_EMAIL") or kindle_section.get("email")

    missing = []
    if not host:
        missing.append("SMTP host")
    if not user:
        missing.append("SMTP user")
    if not password:
        missing.append("SMTP password")
    if not kindle_email:
        missing.append("Kindle email")

    if missing:
        raise ValueError(
            "Missing email configuration: "
            + ", ".join(missing)
            + f". Set environment variables or create {CONFIG_PATH} "
            "(see config.example.ini)."
        )

    return EmailConfig(
        smtp=SmtpConfig(
            host=host,
            port=int(port_raw),
            user=user,
            password=password,
            use_tls=_parse_bool(use_tls_raw, True),
        ),
        kindle_email=kindle_email,
    )
