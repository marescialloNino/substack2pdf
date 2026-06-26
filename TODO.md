# TODO

## EPUB / conversion

- [ ] Test EPUB with images on image-heavy Substack posts (Kindle rendering)
- [ ] Verify Medium articles with `--medium --format epub`
- [ ] **`--usb` flag** — auto-copy EPUB to mounted Kindle `documents/` folder
- [ ] **`--open` flag** — open output folder after conversion

## Code quality

- [ ] Refactor into `core/` package (fetch, epub, pdf) shared by CLI and future webapp
- [ ] Split HTML fetch from format-specific styling (reduce duplication between PDF/EPUB CSS)

## Future (webapp)

- [ ] FastAPI wrapper around conversion core
- [ ] Simple web UI: paste URL → download EPUB
- [ ] See [COMPETITORS.md](COMPETITORS.md) for positioning
