# Suhi's Job Intelligence Hub — Auto-Updating Platform

## What this does
Scrapes **250+ company career pages** every morning across:
- 🟢 **Greenhouse** — 100 companies (Stripe, HubSpot, Coinbase, OpenAI, Datadog, Twilio, Reddit, Notion, Figma, Gusto, Rippling, Amplitude, MongoDB, Robinhood, Plaid, Brex, Ramp, Benchling, Lyft, and 80+ more)
- 🔵 **Lever** — 80 companies (Netflix, Dropbox, Carta, Arcadia.io, Mercury, Headspace, Lyra Health, Lattice, Gem, Modern Treasury, Innovaccer, and 68+ more)
- 🟣 **Ashby** — 40 companies (Linear, Vercel, Retool, Perplexity, Cursor, ElevenLabs, Hugging Face, Weights & Biases, Scale AI, Descript, and 30+ more)
- 🟠 **Workday** — 30 companies (Fidelity, JPMorgan, Capital One, Ally Financial, AT&T, Salesforce, Oracle, Deloitte, McKinsey, Accenture, Southwest Airlines, Toyota, and 18+ more)

**All free. No API keys needed. Runs automatically every day at 8am CST.**

---

## Setup — 4 steps, ~10 minutes

### Step 1: Create a GitHub account (if you don't have one)
Go to https://github.com/signup — it's free.

### Step 2: Create a new repository
1. Go to https://github.com/new
2. Name it: `suhi-job-hub` (or anything you like)
3. Set it to **Public**
4. Click **Create repository**

### Step 3: Upload these files
Upload this entire folder structure to your repo:
```
suhi_platform/
├── .github/
│   └── workflows/
│       └── daily-scrape.yml    ← GitHub Actions automation
├── src/
│   ├── scraper.py              ← Fetches all jobs
│   └── build_html.py           ← Builds the HTML platform
├── docs/
│   ├── jobs.json               ← Auto-generated (don't edit)
│   └── index.html              ← Auto-generated (don't edit)
└── README.md
```

The easiest way: drag and drop the files at github.com/YOUR_USERNAME/suhi-job-hub

### Step 4: Enable GitHub Pages
1. Go to your repo → Settings → Pages
2. Source: **Deploy from a branch**
3. Branch: **main**, Folder: **/docs**
4. Click Save

Your platform will be live at:
**https://YOUR_USERNAME.github.io/suhi-job-hub**

---

## First run (get jobs immediately)
Don't wait for the scheduled 8am run:
1. Go to your repo → **Actions** tab
2. Click **Daily Job Scraper** on the left
3. Click **Run workflow** → **Run workflow**
4. Wait ~2 minutes
5. Refresh your GitHub Pages URL — jobs will be there!

---

## How it auto-updates
- GitHub Actions runs the scraper at **8:00 AM CST every day** (free, no setup needed)
- Calls Greenhouse/Lever/Ashby public APIs (no auth needed)
- Scrapes Workday via internal search endpoint
- Scores every job against your resume profile
- Saves top 100 matching jobs to `docs/jobs.json`
- Rebuilds `docs/index.html`
- Commits and pushes the update
- Your GitHub Pages URL shows fresh jobs automatically

**Total cost: $0. GitHub Actions gives you 2,000 free minutes/month. This uses ~5 minutes per day.**

---

## Adding more companies
To add a company, find which ATS they use:

**Find Greenhouse token:**
Visit `https://boards.greenhouse.io/COMPANY_NAME`
If it works, add `("COMPANY_NAME", "Display Name")` to `GREENHOUSE_COMPANIES` in scraper.py

**Find Lever token:**
Visit `https://jobs.lever.co/COMPANY_NAME`
If it works, add `("COMPANY_NAME", "Display Name")` to `LEVER_COMPANIES`

**Find Ashby token:**
Visit `https://jobs.ashbyhq.com/COMPANY_NAME`
If it works, add `("COMPANY_NAME", "Display Name")` to `ASHBY_COMPANIES`

**Find Workday URL:**
Search Google: `COMPANY_NAME myworkdayjobs.com`
Add the URL to `WORKDAY_COMPANIES`

---

## Running locally (optional)
```bash
pip install requests
python src/scraper.py    # fetches jobs → docs/jobs.json
python src/build_html.py # builds → docs/index.html
python3 -m http.server 8080 --directory docs
# Open http://localhost:8080
```

---

## Notes
- LinkedIn messages must be copied and sent manually (LinkedIn API is closed)
- AI Tailor and Outreach drafting work when opened via http:// (not file://)
- Run `python3 -m http.server 8080` in the docs/ folder for full local functionality
