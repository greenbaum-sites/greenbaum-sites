# Greenbaum Sites — Cowork Deployment Handoff
## February 2, 2026

---

## WHAT THIS IS

Four static websites that form a unified personal and professional web presence for Justin R. Greenbaum. All four share a cohesive design language (dark theme, Cormorant Garamond / JetBrains Mono / Instrument Sans typography, scroll animations, film grain overlay) but each has its own identity, audience, and accent palette. They cross-link to each other to form a single ecosystem.

All four are pure static HTML/CSS/JS — no frameworks, no build step, no server-side rendering, no databases. They deploy as-is.

---

## THE FOUR SITES

### 1. justingreenbaum.com — The Person
- **Purpose:** Professional hub. Advisory work, Coherence framework, AI governance, Substack essays, Comcast background.
- **Accent:** Gold (#c9a84c)
- **Current hosting:** Squarespace (to be replaced)
- **Files:** `justingreenbaum.com/index.html`
- **External dependencies:** Google Fonts CDN only
- **Images:** None local — pulls from Squarespace CDN for the System Navigation Map (can be replaced later)
- **Links out to:** greenbaumphotography.com, megabrixels.com, LinkedIn, Substack

### 2. greenbaumphotography.com — The Eye
- **Purpose:** Photography portfolio. Published work, series, gear, Leica system.
- **Accent:** Gold (#c9a84c)
- **Current hosting:** Squarespace (to be replaced)
- **Files:** `greenbaumphotography.com/index.html` + 4 local images (photo_eiffel.jpeg, photo_cabinet.jpeg, photo_turntable.jpeg, photo_ships.jpeg)
- **External dependencies:** Google Fonts CDN + Squarespace CDN for portfolio series images
- **Images note:** The portfolio grid currently pulls images from the existing Squarespace CDN URLs. These will continue to work even after Squarespace hosting is replaced, but should eventually be migrated to local/self-hosted images for full independence.
- **Links out to:** megabrixels.com, Instagram (@byjustinrg)

### 3. megabrixels.com — The Studio
- **Purpose:** Lego fine art photography studio brand. Nine Worlds, gear, manifesto.
- **Accent:** Gold (#c9a84c)
- **Current hosting:** WordPress (to be replaced)
- **Files:** `megabrixels.com/index.html` + 6 local images (photo_eiffel.jpeg, photo_cabinet.jpeg, photo_turntable.jpeg, photo_ships.jpeg, photo_studio.jpeg, photo_eiffel_full.jpeg)
- **External dependencies:** Google Fonts CDN only
- **Links out to:** Instagram (@megabrixels, @byjustinrg)

### 4. greenbaumlabs.com — The Workshop
- **Purpose:** Personal AI lab. DGX Spark infrastructure, side projects (RC Pit Boss, Coherence engine, planned builds), operating principles.
- **Accent:** Green (#5dba5d) — terminal/workbench aesthetic
- **Current hosting:** None (new domain, needs to be registered if not already owned)
- **Files:** `greenbaumlabs.com/index.html`
- **External dependencies:** Google Fonts CDN only
- **Links out to:** justingreenbaum.com, greenbaumphotography.com, megabrixels.com, rcpitboss.com, LinkedIn, Substack, GitHub

---

## REPO STRUCTURE

```
greenbaum-sites/
├── COWORK-HANDOFF.md          ← This file
├── README.md                  ← Repo readme
├── justingreenbaum.com/
│   └── index.html
├── greenbaumphotography.com/
│   ├── index.html
│   ├── photo_cabinet.jpeg
│   ├── photo_eiffel.jpeg
│   ├── photo_ships.jpeg
│   └── photo_turntable.jpeg
├── megabrixels.com/
│   ├── index.html
│   ├── photo_cabinet.jpeg
│   ├── photo_eiffel.jpeg
│   ├── photo_eiffel_full.jpeg
│   ├── photo_ships.jpeg
│   ├── photo_studio.jpeg
│   └── photo_turntable.jpeg
└── greenbaumlabs.com/
    └── index.html
```

---

## DEPLOYMENT PLAN

### Option A: Vercel (Recommended)

Vercel free tier supports multiple projects with custom domains. Each site becomes its own Vercel project pointing to a subdirectory of the same GitHub repo.

**Step 1: Create GitHub repo**
```bash
cd greenbaum-sites
git init
git add .
git commit -m "Initial commit: four-site portfolio ecosystem"
git remote add origin https://github.com/justingreenbaum/greenbaum-sites.git
git push -u origin main
```

**Step 2: Create four Vercel projects**

For each site, create a new project in Vercel dashboard (vercel.com):
1. Import the `greenbaum-sites` repo from GitHub
2. Set the **Root Directory** to the site's folder name:
   - Project 1: Root Directory = `justingreenbaum.com`
   - Project 2: Root Directory = `greenbaumphotography.com`
   - Project 3: Root Directory = `megabrixels.com`
   - Project 4: Root Directory = `greenbaumlabs.com`
3. Framework Preset: **Other** (these are static HTML, no framework)
4. Build Command: Leave empty (no build step needed)
5. Output Directory: `.` (root of each subdirectory)

**Step 3: Add custom domains**

In each Vercel project's Settings → Domains:
- Project 1: Add `justingreenbaum.com` and `www.justingreenbaum.com`
- Project 2: Add `greenbaumphotography.com` and `www.greenbaumphotography.com`
- Project 3: Add `megabrixels.com` and `www.megabrixels.com`
- Project 4: Add `greenbaumlabs.com` and `www.greenbaumlabs.com`

Vercel will provide DNS records (either CNAME or A records) to configure at your domain registrar.

**Step 4: Update DNS at domain registrar**

For each domain, update DNS to point to Vercel:
- A Record: `76.76.21.21` (Vercel's IP)
- CNAME for www: `cname.vercel-dns.com`

Or use the specific records Vercel provides in the dashboard.

**Step 5: Verify**

Vercel auto-provisions SSL certificates. After DNS propagation (usually 5-30 minutes, sometimes up to 48 hours), all four sites will be live with HTTPS.

### Option B: Netlify (Alternative)

Same process, different platform. Netlify also supports multiple sites from one repo with custom domains on the free tier. The only difference is the dashboard UX and the DNS records they provide.

### Option C: GitHub Pages (Simplest but limited)

GitHub Pages only supports one custom domain per repo. You'd need four separate repos. Works but less elegant. Not recommended for this use case.

---

## DNS CONFIGURATION CHECKLIST

Before deploying, confirm ownership/access to all four domains:

| Domain | Registrar | Status |
|--------|-----------|--------|
| justingreenbaum.com | ? | Currently on Squarespace — need to update DNS |
| greenbaumphotography.com | ? | Currently on Squarespace — need to update DNS |
| megabrixels.com | ? | Currently on WordPress — need to update DNS |
| greenbaumlabs.com | ? | **May need to be registered** — confirm ownership |

**Important:** When moving justingreenbaum.com and greenbaumphotography.com away from Squarespace, you may need to:
1. Check if the domain was purchased through Squarespace (in which case DNS is managed there) or through a separate registrar
2. If through Squarespace, either transfer the domain out or just update the DNS records while keeping the domain registered there
3. If through a separate registrar (GoDaddy, Namecheap, Google Domains, etc.), just update the DNS records

Same for megabrixels.com with WordPress/the WordPress hosting provider.

---

## CURRENT SQUARESPACE/WORDPRESS CONTENT TO PRESERVE

### greenbaumphotography.com (Squarespace)
- Portfolio images are served from Squarespace CDN (images.squarespace-cdn.com)
- The new site references these CDN URLs directly — they will continue to work even after DNS changes
- **Long-term:** Download all portfolio images from Squarespace and host them locally in the repo or on a CDN you control
- Blog posts exist on the current site — these are not replicated in the new static site
- Email: justin@greenbaumphotography.com — verify this is hosted independently of Squarespace (if through Squarespace, you'll need to migrate email separately)

### justingreenbaum.com (Squarespace)
- System Navigation Map image is served from Squarespace CDN
- Substack essays are linked externally (no migration needed)
- Email: hi@justingreenbaum.com — same email hosting concern as above

### megabrixels.com (WordPress)
- Current content is template placeholder — nothing to preserve
- Just needs DNS update

---

## POST-DEPLOYMENT VERIFICATION

After all four sites are live, verify:

1. [ ] justingreenbaum.com loads correctly with HTTPS
2. [ ] greenbaumphotography.com loads correctly with HTTPS
3. [ ] megabrixels.com loads correctly with HTTPS
4. [ ] greenbaumlabs.com loads correctly with HTTPS
5. [ ] All cross-site links work (click every link between sites)
6. [ ] Portfolio images load on greenbaumphotography.com (from Squarespace CDN)
7. [ ] Local images load on megabrixels.com and greenbaumphotography.com
8. [ ] Scroll animations fire on all four sites
9. [ ] Mobile responsive on all four sites
10. [ ] Email links work (mailto: on each site)
11. [ ] External links work (Instagram, LinkedIn, Substack, GitHub, rcpitboss.com)
12. [ ] www redirects work (www.domain.com → domain.com or vice versa)

---

## FUTURE IMPROVEMENTS (NOT IN SCOPE FOR THIS DEPLOYMENT)

These are noted for context but should NOT be done during initial deployment:

1. **Migrate Squarespace CDN images** — Download all portfolio images and host locally
2. **Add favicon and OG meta images** — Each site needs a favicon.ico and Open Graph images for social sharing
3. **Add Google Analytics or Plausible** — Privacy-friendly analytics to track traffic
4. **greenbaumphotography.com blog** — If blog content is wanted, could add a /blog page or link to a Substack
5. **greenbaumlabs.com project pages** — Individual project detail pages as projects mature
6. **Mobile nav menu** — All four sites have a hamburger icon on mobile but no slide-out menu wired up yet (the nav links are just hidden). This needs JS to toggle visibility.
7. **SEO optimization** — Sitemap.xml, robots.txt, structured data for each site
8. **Email hosting verification** — Ensure email addresses work independently of Squarespace/WordPress hosting

---

## COST

| Item | Cost |
|------|------|
| GitHub (Free) | $0 |
| Vercel (Hobby/Free) | $0 |
| Domain renewals (4 domains) | ~$50-60/year total (already being paid) |
| greenbaumlabs.com registration (if needed) | ~$12/year |
| **Total new cost** | **$0 — $12/year** |

---

## SUMMARY

Four static HTML sites. One GitHub repo. Four Vercel projects. Four custom domains. Zero build steps. Zero monthly cost. Push to main and everything deploys.

The sites are production-ready. The only work is: create the repo, set up Vercel projects, point DNS, and verify.
