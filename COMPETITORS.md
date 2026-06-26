# Competitors

Landscape for Substack/article → Kindle (and e-reader) tools. Last updated: June 2026.

---

## Direct competitors — Substack / newsletters → Kindle

### 1. InboxToKindle

- **Links:** [inboxtokindle.com](https://inboxtokindle.com/) · [Substack page](https://inboxtokindle.com/substack-to-kindle/) · [How-to guide](https://inboxtokindle.com/how-to/read-substack-kindle/)
- **Model:** Subscribe to newsletters using *their* anonymous email address
- **Flow:** Substack → their inbox → strip ads → EPUB → Kindle (via Amazon email)
- **Substack:** Dedicated landing page; works with free + paid subs
- **Formats:** EPUB
- **Devices:** Kindle, Boox
- **Pricing:** Free: 15 deliveries/mo · Pro: **$10/mo** unlimited
- **Scraping?** No — receives newsletter emails
- **vs us:** Ongoing subscription inbox; we do one-shot URL → file

---

### 2. readinbox

- **Links:** [readinbox.io](https://readinbox.io/) · [Pricing](https://readinbox.io/pricing) · [Substack guide](https://readinbox.io/read-substack-on-kindle)
- **Model:** Forward newsletters to a personal `@readinbox` address
- **Flow:** Email forward → clean EPUB/PDF → Kindle (email) or Kobo/PocketBook/BOOX/reMarkable (Dropbox/Drive)
- **Platforms:** Substack, Beehiiv, ConvertKit, Mailchimp, Ghost, Buttondown, etc.
- **Formats:** EPUB, PDF
- **Pricing:** Free: 5 newsletters/mo, 1 device · Reader: **$8/mo** (50/mo) · Library: **$14/mo** unlimited
- **Scraping?** No — email-based
- **vs us:** Multi-device (not just Kindle); newsletter-forward model

---

### 3. KTool

- **Links:** [ktool.io](https://ktool.io/) · [Pricing](https://ktool.io/pricing) · [Docs](https://docs.ktool.io/feature-list) · [Chrome extension](https://chromewebstore.google.com/detail/send-web-articles-to-kind/igfcoofpmcdpcocfofdobneaileiogmo)
- **Model:** Browser extension + mobile app + web “Quick Send”
- **Flow:** Click “Send to Kindle” on any page, or forward newsletters to `@inbox.ktool.io`
- **Content:** Web articles, Twitter threads, Wikipedia, StackOverflow, RSS, newsletters, PDF/DOCX/Markdown
- **Substack:** RSS support; newsletter forwarding (Premium)
- **Formats:** EPUB (modern), digests/magazines
- **Devices:** Kindle, Kindle app; beta Kobo via Dropbox
- **Pricing:** 7-day trial · Basic **$4.99/mo** (articles) · Premium **$6.99/mo** (newsletters, RSS) · Platinum **$10/mo** (EPUB download, docs)
- **Scraping?** Yes — fetches URLs server-side; claims paywall support
- **vs us:** Closest overall competitor; broader scope, paid, extension-first

---

### 4. Readivio

- **Links:** [readivio.com](https://readivio.com/) · [Pricing](https://readivio.com/pricing)
- **Model:** Web app — paste URL, RSS, forward newsletter, or upload PDF
- **Flow:** Convert → send to Kindle/Kobo/PocketBook
- **Features:** RSS feeds, newsletter forwarding, daily digests, on-demand URL send
- **Pricing:** Free: 10 articles/mo, 1 RSS feed · Pro: **$9/mo** unlimited
- **Scraping?** Yes for URLs; email path for newsletters
- **vs us:** Similar webapp vision; multi-device, RSS-heavy

---

## Direct competitors — any web article → Kindle

### 5. Push to Kindle (FiveFilters)

- **Links:** [pushtokindle.com](https://www.pushtokindle.com/) · [Chrome extension](https://chromewebstore.google.com/detail/push-to-kindle/pnaiinchjaonopoejhknmgjingcnaloc) · [iOS](https://apps.apple.com/us/app/push-to-kindle-by-mochi/id1642144176) · [Android](https://play.google.com/store/apps/details?id=org.fivefilters.pushtokindle)
- **Model:** Browser extension + mobile apps + web
- **Flow:** Extract article → EPUB → Kindle app share OR `@kindle.com` email
- **Delivery:** Default: share EPUB via official Kindle app (no email setup); optional email mode
- **Also supports:** Apple Books, Dropbox, PocketBook
- **Pricing:** Free: 10 articles/mo · Premium: **~$2.99–4.99/mo** or **$34.99/yr** unlimited
- **Scraping?** Yes — server-side extraction
- **vs us:** Mature, polished; any article, not Substack-specific

---

### 6. EpubPress

- **Links:** [epub.press](https://epub.press/) · [GitHub](https://github.com/haroldtreen/epub-press)
- **Model:** Browser extension — bundle tabs into one ebook
- **Flow:** Open tabs → select → download EPUB/MOBI or email to Kindle (`epubpress@gmail.com` as sender)
- **Formats:** EPUB, MOBI
- **Pricing:** Free (donation-supported)
- **Scraping?** Yes
- **vs us:** Multi-article bundling; older project, less Substack focus

---

### 7. Amazon Send to Kindle (official)

- **Links:** [amazon.com/sendtokindle](https://www.amazon.com/sendtokindle) · [Email help](https://www.amazon.com/sendtokindle/email)
- **Model:** Browser extension, desktop app, email
- **Flow:** Send page/file to Kindle library
- **Formats:** PDF, DOC, EPUB, HTML, images, etc.
- **Pricing:** Free
- **Scraping?** Amazon handles extraction (extension)
- **vs us:** Free, official; generic formatting, no Substack tuning

---

## Adjacent — read-later → Kindle

### 8. Instapaper

- **Link:** [instapaper.com](https://www.instapaper.com/)
- **Model:** Save articles → read later → optional Kindle delivery
- **Kindle:** Approve Instapaper sender; auto or manual batch send
- **Pricing:** Freemium · Premium ~**$2.99/mo** (Kindle auto-send, etc.)
- **Substack:** Save individual posts manually
- **vs us:** Inbox/queue model, not one-shot Substack converter

---

### 9. Pocket

- **Link:** [getpocket.com](https://getpocket.com/)
- **Model:** Save-for-later
- **Kindle:** Weak/indirect — export or third-party bridges
- **Pricing:** Freemium
- **vs us:** Not really a Kindle delivery competitor

---

### 10. Omnivore / Matter

- **Links:** [omnivore.app](https://omnivore.app/) · [getmatter.com](https://getmatter.com/)
- **Model:** Modern read-later apps
- **Kindle:** Limited or deprecated Kindle features
- **vs us:** Compete on reading UX, not Substack → Kindle pipeline

---

## Local / DIY (no service)

### 11. Calibre

- **Link:** [calibre-ebook.com](https://calibre-ebook.com/)
- **Model:** Desktop app
- **Flow:** Download/recipe → convert → USB or email to Kindle
- **Pricing:** Free, open source

---

## Comparison matrix

| Product | Substack-specific | One-shot URL | Newsletter auto | Kindle send | Free tier | Paid |
|---------|-------------------|--------------|-----------------|-------------|-----------|------|
| **substack2pdf (us)** | ✅ | ✅ | ❌ | Manual (USB / Amazon) | ✅ | Free |
| **InboxToKindle** | ✅ | ❌ | ✅ | ✅ (their email) | 15/mo | $10/mo |
| **readinbox** | ✅ | ❌ | ✅ | ✅ | 5/mo | $8–14/mo |
| **KTool** | Partial | ✅ | ✅ (paid) | ✅ | 7-day trial | $5–10/mo |
| **Readivio** | Partial | ✅ | ✅ (paid) | ✅ | 10/mo | $9/mo |
| **Push to Kindle** | ❌ | ✅ | ❌ | ✅ | 10/mo | ~$3–5/mo |
| **EpubPress** | ❌ | ✅ | ❌ | Optional | ✅ | Free |
| **Amazon STK** | ❌ | ✅ | ❌ | ✅ | ✅ | Free |
| **Instapaper** | Manual | Manual save | Digest | ✅ | Limited | ~$3/mo |

---

## Closest

1. **[KTool](https://ktool.io/)** — same job (URL → Kindle), more features, paid
2. **[InboxToKindle](https://inboxtokindle.com/substack-to-kindle/)** — owns Substack *subscription* use case
3. **[Push to Kindle](https://www.pushtokindle.com/)** — polished, cheap, any article
4. **[Readivio](https://readivio.com/)** — similar webapp direction (URL + RSS + newsletters)

---
