# livOsax

Olivia’s alto saxophone website, hosted at https://livosax.com/ with GitHub Pages.

## Develop and publish

Python 3.9+ is the only build dependency.

```sh
python3 scripts/build.py
python3 -m http.server 8765 --directory dist
```

Push to `main` to build and deploy through `.github/workflows/deploy.yml`.
Only `dist/` is published. Source files, scripts and design notes are not served.

## Videos

`videos.json` contains the eight public channel videos verified on 18 September 2026, including titles, durations, public publication timestamps and descriptions from YouTube. Add new **public** videos to this file and run the build. Private/unlisted videos must not be added without an explicit request. This version does not automatically sync future uploads.

Each video has a dedicated `/videos/<slug>/` page, a visible embedded player, canonical URL, unique metadata, VideoObject and BreadcrumbList JSON-LD, descriptive text, question-and-answer content and links to the other performances. The home page keeps a lightweight click-to-load player. No fabricated transcripts, reviews, statistics or lesson claims are used.

The sitemap contains the homepage plus eight video entries. `robots.txt` references it. IndexNow verification is public by design: `indexnow-key.txt` supplies the generated root key file. After deployment and HTTPS verification, run `python3 scripts/indexnow.py` to notify participating search engines. Acceptance does not guarantee indexing.

## Domains

- `livosax.com`: main repository `ostapenko-studio/livosax`.
- `www.livosax.com`: CNAME to `ostapenko-studio.github.io`; GitHub redirects it to the apex.
- `livosax.au`: `ostapenko-studio/livosax-au-redirect`.
- `livosax.com.au`: `ostapenko-studio/livosax-com-au-redirect`.

The two redirect checkouts are inside ignored `redirects/`. They use immediate HTML refresh with a JavaScript fallback, matching the existing Ostapenko Studio redirect approach. GitHub Pages does not provide custom server-side 301 rules. Both redirect sites declare the `.com` canonical and `noindex`.

DNS is managed at Crazy Domains. Apex A records use GitHub’s four addresses: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153. Existing Google Workspace MX and verification TXT records on `.com` are preserved.

## Design

Existing navy/gold channel identity with Avenir Next/system font stack. Responsive layout, keyboard focus, reduced motion support, semantic headings, native dialog, external-player fallback, and lightweight static HTML/CSS/JavaScript.

Design canvas: https://superdesign.dev/teams/8aa2ecc4-bfb6-4544-9d40-452467b23f37/projects/52d03ac3-3f23-4571-9dfe-f351ff622b53
