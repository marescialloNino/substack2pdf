# TODO

## Kindle email delivery

- [ ] **Fix SMTP provider setup** — Gmail app passwords blocked for some accounts ("setting not available"). Document and test alternatives:
  - Outlook.com (`smtp-mail.outlook.com`)
  - Zoho Mail (`smtp.zoho.com`)
  - Brevo / other relay with separate `smtp_login` vs `from_email` (requires code change)
- [ ] **Improve SMTP error messages** — distinguish Gmail BadCredentials vs Amazon sender-not-approved vs attachment too large
- [ ] **Add `smtp_login` / `from_email` split in config** — needed for relay providers like Brevo where login ≠ From address
- [ ] **Document Gmail app-password unavailability** — note that new/restricted Google accounts may not get the option at all
- [ ] **End-to-end test** — verify `--send-email` delivers to Kindle with working provider credentials

## EPUB / conversion

- [ ] Test EPUB with images on a real Substack post (image embedding + Kindle rendering)
- [ ] Verify Medium articles work for EPUB + email flow

## Docs

- [ ] Add Outlook/Zoho setup examples to README (alongside Gmail)
- [ ] Add Italian-language troubleshooting section for email setup (optional)
