# Greenbaum Sites

Four-site portfolio ecosystem for Justin R. Greenbaum. Static HTML, no build step, deployed on Vercel.

## Sites

| Site | Directory | Domain | Accent |
|------|-----------|--------|--------|
| Professional hub | `justingreenbaum.com/` | justingreenbaum.com | Gold (#c9a84c) |
| AI workshop | `greenbaumlabs.com/` | greenbaumlabs.com | Green (#5dba5d) |
| Photography | `greenbaumphotography.com/` | greenbaumphotography.com | Gold (#c9a84c) |
| Lego art studio | `megabrixels.com/` | megabrixels.com | Gold (#c9a84c) |

## Stack

- Pure HTML + CSS + vanilla JS — no frameworks, no dependencies, no build step
- Google Fonts via CDN (Cormorant Garamond, JetBrains Mono, Instrument Sans)
- Deployed on Vercel with `"cleanUrls": true` in `vercel.json`
- Each site is a separate Vercel project pointing to its subdirectory

## Critical: Clean URLs

Vercel is configured with `"cleanUrls": true`. This means:
- Pages are served at `/about`, NOT `/about.html`
- **Never use `.html` extensions in href links, canonical URLs, og:url, twitter:url, or JSON-LD**
- Use `/` instead of `index.html` for home page links
- Use `/#section` instead of `index.html#section` for anchor links
- Sitemaps must also use clean URLs (no `.html`)

## Repo Structure

```
greenbaum-sites/
├── vercel.json                    # Vercel config (cleanUrls: true)
├── sitemap.xml                    # justingreenbaum.com sitemap
├── justingreenbaum.com/
│   ├── index.html                 # Landing page
│   ├── about.html                 # About page
│   ├── coherence.html             # Coherence intro
│   ├── coherence-deep.html        # Deep dive on Coherence
│   ├── decision-responsibility-infrastructure.html
│   └── sitemap.xml
├── greenbaumlabs.com/
│   ├── index.html                 # Landing page
│   ├── agentforce.html            # Agentforce page
│   ├── field.html                 # The Field — tool orientation
│   ├── case-study-diagnostic-engine.html
│   ├── sitemap.xml
│   └── tools/                     # 7 diagnostic instruments
│       ├── declaration-log.html
│       ├── fm-scanner.html
│       ├── ffn-surface.html
│       ├── regression-watch.html
│       ├── system-nav-locator.html
│       ├── verified-independence.html
│       └── continuity-chain.html
├── greenbaumphotography.com/
│   ├── index.html
│   └── (photo assets)
└── megabrixels.com/
    ├── index.html
    └── (photo assets)
```

## Git

- Owner: Justin Greenbaum <justin@greenbaumlabs.com>
- Remote: https://github.com/greenbaum-sites/greenbaum-sites.git
- Branch: main
- Deploys automatically on push to main via Vercel
