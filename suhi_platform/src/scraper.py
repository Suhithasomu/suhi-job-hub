"""
Suhi's Job Intelligence Platform - Multi-ATS Scraper
Fetches from: Greenhouse (100+ companies), Lever (80+ companies),
              Ashby (40+ companies), Workday (30+ companies), Indeed API

Runs free on GitHub Actions daily. Outputs docs/jobs.json + docs/index.html
"""

import requests, json, time, re, os
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

# ─── RESUME PROFILE (scoring weights) ───────────────────────────────────────
PROFILE_SKILLS = {
    "sql":10, "python":10, "tableau":9, "power bi":8, "snowflake":9,
    "dbt":8, "alteryx":8, "spark":7, "kafka":7, "databricks":7,
    "aws":8, "etl":9, "elt":8, "a/b testing":8, "analytics":9,
    "data analyst":10, "data engineer":8, "machine learning":6,
    "healthcare":8, "fintech":8, "saas":8, "ecommerce":7,
    "revenue":8, "pricing":8, "bi":8, "looker":7, "airflow":6,
    "redshift":7, "bigquery":7, "excel":6, "r":5, "scala":4,
}
TARGET_TITLES = [
    "data analyst", "senior data analyst", "analytics engineer",
    "data engineer", "business analyst", "bi analyst",
    "business intelligence", "revenue analyst", "product analyst",
    "insights analyst", "reporting analyst", "data scientist"
]
EXCLUDE_TITLES = [
    "staff engineer", "principal engineer", "vp ", "director ",
    "legal", "attorney", "lawyer", "sales representative",
    "customer success", "account manager", "marketing manager",
    "recruiter", "hr ", "administrative", "coordinator",
    "graphic design", "ux design", "physical therapist",
    "nurse", "physician", "clinical", "driver", "warehouse",
    "mechanic", "plumber", "electrician", "chef", "cook"
]

# ─── GREENHOUSE COMPANIES (100 curated, data/analytics relevant) ─────────────
GREENHOUSE_COMPANIES = [
    # FinTech
    ("stripe","Stripe"), ("robinhood","Robinhood"), ("coinbase","Coinbase"),
    ("brex","Brex"), ("ramp","Ramp"), ("plaid","Plaid"),
    ("chime","Chime"), ("affirm","Affirm"), ("marqeta","Marqeta"),
    ("blend","Blend"), ("carta","Carta"), ("ripple","Ripple"),
    ("stax","Stax"), ("greenlight","Greenlight"), ("paylocity","Paylocity"),
    # Healthcare
    ("oscar","Oscar Health"), ("cityblock","Cityblock Health"),
    ("tempus","Tempus"), ("veeva","Veeva Systems"),
    ("hims","Hims & Hers"), ("noom","Noom"),
    ("privia","Privia Health"), ("zelis","Zelis"),
    ("aledade","Aledade"), ("waystar","Waystar"),
    # SaaS / Tech
    ("hubspot","HubSpot"), ("zendesk","Zendesk"), ("twilio","Twilio"),
    ("elastic","Elastic"), ("mongodb","MongoDB"), ("hashicorp","HashiCorp"),
    ("cloudflare","Cloudflare"), ("datadog","Datadog"), ("fastly","Fastly"),
    ("pagerduty","PagerDuty"), ("sendgrid","SendGrid"),
    ("segment","Segment"), ("miro","Miro"), ("notion","Notion"),
    ("figma","Figma"), ("invision","InVision"), ("lattice","Lattice"),
    ("rippling","Rippling"), ("gusto","Gusto"), ("lever","Lever"),
    ("greenhouse","Greenhouse Software"), ("workato","Workato"),
    ("talkdesk","Talkdesk"), ("klaviyo","Klaviyo"), ("iterable","Iterable"),
    ("amplitude","Amplitude"), ("mixpanel","Mixpanel"),
    ("heap","Heap Analytics"), ("sisense","Sisense"), ("looker","Looker"),
    # E-Commerce / Retail
    ("doordash","DoorDash"), ("instacart","Instacart"),
    ("gopuff","GoPuff"), ("shipt","Shipt"),
    ("returnly","Returnly"), ("yotpo","Yotpo"),
    # Media / Other Tech
    ("reddit","Reddit"), ("tripadvisor","TripAdvisor"),
    ("github","GitHub"), ("gitlab","GitLab"),
    ("dropbox","Dropbox"), ("box","Box"),
    ("zenefits","Zenefits"), ("rippling","Rippling"),
    ("postmates","Postmates"), ("lyft","Lyft"),
    ("openai","OpenAI"), ("scale","Scale AI"),
    ("anthropic","Anthropic"), ("cohere","Cohere"),
    # Consulting / Analytics
    ("domo","Domo"), ("tableau","Tableau"),
    ("matillion","Matillion"), ("fivetran","Fivetran"),
    ("airbyte","Airbyte"), ("dbt","dbt Labs"),
    ("hightouch","Hightouch"), ("rudderstack","RudderStack"),
    ("census","Census"), ("metabase","Metabase"),
    ("mode","Mode Analytics"), ("sigma","Sigma Computing"),
    # Dallas-area + Remote Friendly
    ("match","Match Group"), ("at&t","AT&T"),
    ("toyota","Toyota Connected"), ("amdocs","Amdocs"),
    ("dialexa","Dialexa"), ("resultant","Resultant"),
    # Additional High-Value
    ("nerdwallet","NerdWallet"), ("betterment","Betterment"),
    ("sofi","SoFi"), ("lemonade","Lemonade"),
    ("hippo","Hippo Insurance"), ("ethos","Ethos Life"),
    ("policygenius","PolicyGenius"), ("kin","Kin Insurance"),
    ("clearcover","ClearCover"), ("roots","Roots Insurance"),
    ("benchling","Benchling"), ("veracyte","Veracyte"),
    ("flatiron","Flatiron Health"), ("zocdoc","ZocDoc"),
    ("olive","Olive AI"), ("arcadia","Arcadia"),
    ("healthsun","HealthSun"), ("alignment","Alignment Healthcare"),
    ("phreesia","Phreesia"), ("doceree","Doceree"),
]

# ─── LEVER COMPANIES (80 curated) ──────────────────────────────────────────
LEVER_COMPANIES = [
    # FinTech
    ("mercury","Mercury"), ("brex","Brex"),
    ("moderntreasury","Modern Treasury"), ("teller","Teller"),
    ("unit","Unit"), ("synctera","Synctera"),
    ("lithic","Lithic"), ("column","Column"),
    ("treasury-prime","Treasury Prime"), ("bond","Bond"),
    # Healthcare
    ("arcadia","Arcadia.io"), ("innovaccer","Innovaccer"),
    ("health-gorilla","Health Gorilla"), ("ribbon","Ribbon Health"),
    ("stellar-health","Stellar Health"), ("alma","Alma"),
    ("headspace","Headspace"), ("cerebral","Cerebral"),
    ("brightline","Brightline"), ("lyra","Lyra Health"),
    # SaaS
    ("lattice","Lattice"), ("gem","Gem"),
    ("ashby","Ashby"), ("notion","Notion"),
    ("retool","Retool"), ("linear","Linear"),
    ("vercel","Vercel"), ("fly","Fly.io"),
    ("planetscale","PlanetScale"), ("supabase","Supabase"),
    ("neon","Neon Database"), ("render","Render"),
    ("railway","Railway"), ("dagger","Dagger"),
    # Data / Analytics
    ("rockset","Rockset"), ("imply","Imply Data"),
    ("starburst","Starburst"), ("alluxio","Alluxio"),
    ("celerdata","CelerData"), ("motherduck","MotherDuck"),
    ("turbopuffer","Turbopuffer"), ("epsio","Epsio"),
    ("cube","Cube.js"), ("rill","Rill Data"),
    ("evidence","Evidence"), ("lightdash","Lightdash"),
    ("hex","Hex Technologies"), ("deepnote","Deepnote"),
    # E-Commerce / Consumer
    ("faire","Faire"), ("glossier","Glossier"),
    ("allbirds","Allbirds"), ("warby-parker","Warby Parker"),
    ("outdoor-voices","Outdoor Voices"),
    # Other Tech
    ("figma","Figma"), ("loom","Loom"),
    ("pitch","Pitch"), ("mural","MURAL"),
    ("whimsical","Whimsical"), ("maze","Maze"),
    ("usertesting","UserTesting"), ("fullstory","FullStory"),
    ("hotjar","Hotjar"), ("contentsquare","ContentSquare"),
    ("amplitude","Amplitude"), ("posthog","PostHog"),
    ("june","June Analytics"), ("koala","Koala"),
    ("toplyne","Toplyne"), ("pendo","Pendo"),
    # Staffing / Recruiting Tech
    ("greenhouse","Greenhouse"), ("ashby","Ashby"),
    ("dover","Dover"), ("findem","Findem"),
    ("fetcher","Fetcher"), ("humanly","Humanly"),
    ("beamery","Beamery"), ("eightfold","Eightfold AI"),
]

# ─── ASHBY COMPANIES (40 curated) ─────────────────────────────────────────
ASHBY_COMPANIES = [
    ("linear","Linear"), ("vercel","Vercel"),
    ("retool","Retool"), ("perplexity","Perplexity AI"),
    ("cursor","Cursor"), ("elevenlabs","ElevenLabs"),
    ("descript","Descript"), ("luma","Luma AI"),
    ("runway","Runway ML"), ("pika","Pika Labs"),
    ("midjourney","Midjourney"), ("character","Character.AI"),
    ("cohere","Cohere"), ("together","Together AI"),
    ("anyscale","Anyscale"), ("modal","Modal"),
    ("baseten","Baseten"), ("replicate","Replicate"),
    ("huggingface","Hugging Face"), ("weights-biases","Weights & Biases"),
    ("determined-ai","Determined AI"), ("scale","Scale AI"),
    ("labelbox","Labelbox"), ("snorkel","Snorkel AI"),
    ("voxel51","Voxel51"), ("encord","Encord"),
    ("clarifai","Clarifai"), ("roboflow","Roboflow"),
    ("groundlight","Groundlight"), ("landing-ai","Landing AI"),
    # High-growth SaaS
    ("liveblocks","Liveblocks"), ("drifting-in-space","Drifting in Space"),
    ("val-town","Val Town"), ("inngest","Inngest"),
    ("trigger","Trigger.dev"), ("resend","Resend"),
    ("loops","Loops"), ("cal","Cal.com"),
    ("documenso","Documenso"), ("ghostwriter","Ghostwriter"),
]

# ─── WORKDAY COMPANIES (scraped via internal API) ─────────────────────────
WORKDAY_COMPANIES = [
    # FinTech / Finance
    ("fidelity.wd5.myworkdayjobs.com/FIDELITY-US","Fidelity Investments"),
    ("jpmorgan.wd5.myworkdayjobs.com/JPMorganCareerSite","JPMorgan Chase"),
    ("ally.wd5.myworkdayjobs.com/ally_recruiting","Ally Financial"),
    ("blackrock.wd1.myworkdayjobs.com/en-US/BlackRock_Careers","BlackRock"),
    ("americanexpress.wd5.myworkdayjobs.com/ExternalCareers","American Express"),
    ("capitalone.wd1.myworkdayjobs.com/Capital_One","Capital One"),
    ("usbank.wd5.myworkdayjobs.com/US_Bank_Careers","U.S. Bank"),
    ("progressive.wd5.myworkdayjobs.com/ProgCareers","Progressive Insurance"),
    # Healthcare
    ("humana.wd5.myworkdayjobs.com/Humana_External_Career_Site","Humana"),
    ("cigna.wd5.myworkdayjobs.com/Cigna_Careers","Cigna"),
    ("aetna.wd5.myworkdayjobs.com/Aetna_Careers","Aetna"),
    ("cvshealth.wd1.myworkdayjobs.com/CVS_Health_Careers","CVS Health"),
    ("unitedhealthgroup.wd5.myworkdayjobs.com/UHG","UnitedHealth Group"),
    ("mckesson.wd5.myworkdayjobs.com/McK","McKesson"),
    # Tech
    ("amazon.jobs","Amazon"), # Amazon uses their own
    ("nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite","NVIDIA"),
    ("salesforce.wd12.myworkdayjobs.com/External_Career_Site","Salesforce"),
    ("workday.wd5.myworkdayjobs.com/Workday","Workday"),
    ("sap.wd3.myworkdayjobs.com/SAP","SAP"),
    ("oracle.wd5.myworkdayjobs.com/Careers","Oracle"),
    # Consulting
    ("deloitte.wd5.myworkdayjobs.com/DeloitteCareers","Deloitte"),
    ("mckinsey.wd5.myworkdayjobs.com/McKinsey","McKinsey & Co"),
    ("accenture.wd3.myworkdayjobs.com/Accenture_Careers","Accenture"),
    ("kpmg.wd5.myworkdayjobs.com/Careers","KPMG"),
    # Dallas-area
    ("att.wd5.myworkdayjobs.com/ATTCareers","AT&T"),
    ("tenet.wd5.myworkdayjobs.com/TenetHealthcareExternal","Tenet Healthcare"),
    ("jacobs.wd5.myworkdayjobs.com/Careers","Jacobs Engineering"),
    ("verizon.wd5.myworkdayjobs.com/External","Verizon"),
    ("southwest.wd5.myworkdayjobs.com/SouthwestAirlinesCareers","Southwest Airlines"),
    ("toyota.wd5.myworkdayjobs.com/TMNA","Toyota North America"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; JobBot/1.0)"}

def score_job(title, description="", company="", location=""):
    """Score a job 0-100 against Suhi's profile."""
    title_l = title.lower()
    desc_l = (description or "").lower()[:2000]
    loc_l = (location or "").lower()

    # Hard exclude
    for ex in EXCLUDE_TITLES:
        if ex in title_l: return 0

    # Must be somewhat relevant
    title_match = any(t in title_l for t in TARGET_TITLES)
    if not title_match: return 0

    score = 50  # base for passing title filter

    # Skill matches in title (high weight)
    for skill, weight in PROFILE_SKILLS.items():
        if skill in title_l: score += weight
    # Skill matches in description (lower weight)
    for skill, weight in PROFILE_SKILLS.items():
        if skill in desc_l: score += weight * 0.3

    # Seniority bonus
    if "senior" in title_l or "sr." in title_l or "sr " in title_l:
        score += 8
    if "lead" in title_l: score += 5
    if "principal" in title_l: score -= 5  # too senior

    # Location bonus
    if "remote" in loc_l or "remote" in title_l: score += 5
    if "dallas" in loc_l or "tx" in loc_l or "irving" in loc_l or "plano" in loc_l:
        score += 5

    # Industry bonus
    for ind in ["health", "fintech", "finance", "saas", "ecommerce"]:
        if ind in desc_l: score += 3; break

    return min(int(score), 99)


def fetch_greenhouse(token, company_name):
    """Fetch jobs from Greenhouse public API."""
    try:
        url = f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs"
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code != 200: return []
        data = r.json()
        jobs = []
        for j in data.get("jobs", []):
            title = j.get("title", "")
            location = j.get("location", {}).get("name", "")
            job_url = j.get("absolute_url", "")
            updated = j.get("updated_at", "")
            sc = score_job(title, "", company_name, location)
            if sc >= 60:
                jobs.append({
                    "title": title, "company": company_name,
                    "location": location, "url": job_url,
                    "score": sc, "source": "Greenhouse",
                    "posted": updated[:10] if updated else "",
                    "industry": infer_industry(title, company_name),
                    "salary": "See posting",
                    "id": str(j.get("id", "")),
                })
        return jobs
    except: return []


def fetch_lever(token, company_name):
    """Fetch jobs from Lever public API."""
    try:
        url = f"https://api.lever.co/v0/postings/{token}?mode=json&limit=100"
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code != 200: return []
        data = r.json()
        if not isinstance(data, list): return []
        jobs = []
        for j in data:
            title = j.get("text", "")
            cats = j.get("categories", {})
            location = cats.get("location", "") or j.get("workplaceType", "")
            job_url = j.get("hostedUrl", j.get("applyUrl", ""))
            created = j.get("createdAt", 0)
            posted = datetime.fromtimestamp(created/1000, tz=timezone.utc).strftime("%Y-%m-%d") if created else ""
            desc = j.get("description", "") or j.get("descriptionPlain", "")
            sc = score_job(title, desc, company_name, location)
            if sc >= 60:
                jobs.append({
                    "title": title, "company": company_name,
                    "location": location, "url": job_url,
                    "score": sc, "source": "Lever",
                    "posted": posted,
                    "industry": infer_industry(title, company_name),
                    "salary": "See posting",
                    "id": j.get("id", ""),
                })
        return jobs
    except: return []


def fetch_ashby(token, company_name):
    """Fetch jobs from Ashby public API."""
    try:
        url = f"https://api.ashbyhq.com/posting-api/job-board/{token}?includeCompensation=true"
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code != 200: return []
        data = r.json()
        jobs = []
        for j in data.get("jobPostings", []):
            title = j.get("title", "")
            location = j.get("location", "")
            job_url = j.get("jobUrl", "")
            posted = j.get("publishedDate", "")[:10] if j.get("publishedDate") else ""
            comp = j.get("compensation", {})
            salary = ""
            if comp:
                mn = comp.get("minValue"); mx = comp.get("maxValue")
                if mn and mx: salary = f"${int(mn):,}–${int(mx):,}"
            sc = score_job(title, "", company_name, location)
            if sc >= 60:
                jobs.append({
                    "title": title, "company": company_name,
                    "location": location or "Remote", "url": job_url,
                    "score": sc, "source": "Ashby",
                    "posted": posted,
                    "industry": infer_industry(title, company_name),
                    "salary": salary or "See posting",
                    "id": j.get("id", ""),
                })
        return jobs
    except: return []


def fetch_workday(workday_url, company_name):
    """Fetch jobs from Workday internal CXS API."""
    try:
        # Workday's internal search endpoint
        base = f"https://{workday_url}" if not workday_url.startswith("http") else workday_url
        # Extract subdomain for API
        match = re.match(r"https?://([^/]+)", base)
        if not match: return []
        host = match.group(1)
        # Build search URL
        search_url = base.rstrip("/") + "/1/search"
        payload = {
            "appliedFacets": {},
            "limit": 20,
            "offset": 0,
            "searchText": "data analyst"
        }
        r = requests.post(search_url, json=payload, headers={
            **HEADERS, "Content-Type": "application/json"
        }, timeout=10)
        if r.status_code != 200: return []
        data = r.json()
        jobs = []
        for j in data.get("jobPostings", []):
            title = j.get("title", "")
            location = j.get("locationsText", "")
            job_url = j.get("externalPath", "")
            if job_url and not job_url.startswith("http"):
                job_url = base.rstrip("/") + job_url
            posted = j.get("postedOn", "")
            sc = score_job(title, "", company_name, location)
            if sc >= 60:
                jobs.append({
                    "title": title, "company": company_name,
                    "location": location, "url": job_url,
                    "score": sc, "source": "Workday",
                    "posted": posted,
                    "industry": infer_industry(title, company_name),
                    "salary": "See posting",
                    "id": j.get("bulletFields", [""])[0] if j.get("bulletFields") else "",
                })
        return jobs
    except: return []


def infer_industry(title, company):
    t = (title + " " + company).lower()
    if any(x in t for x in ["health","medical","clinical","pharma","hospital","patient","care"]): return "Healthcare"
    if any(x in t for x in ["financial","finance","bank","credit","insurance","fintech","payment","invest"]): return "FinTech"
    if any(x in t for x in ["ecommerce","commerce","retail","shop","consumer","marketplace"]): return "E-Commerce"
    if any(x in t for x in ["ai","machine learning","ml","llm","nlp","artificial"]): return "AI/ML"
    return "SaaS/Tech"


def dedupe(jobs):
    seen = set()
    out = []
    for j in jobs:
        key = f"{j['title'].lower().strip()}|{j['company'].lower().strip()}"
        if key not in seen:
            seen.add(key)
            out.append(j)
    return out


def run_all():
    all_jobs = []
    print(f"\n{'='*55}")
    print(f"  Suhi's Job Scraper — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*55}")

    # ── Greenhouse ──
    print(f"\n🟢 Greenhouse ({len(GREENHOUSE_COMPANIES)} companies)...")
    gh_jobs = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(fetch_greenhouse, t, n): (t,n) for t,n in GREENHOUSE_COMPANIES}
        for f in as_completed(futures):
            result = f.result()
            gh_jobs.extend(result)
    print(f"   Found {len(gh_jobs)} matching jobs")
    all_jobs.extend(gh_jobs)

    # ── Lever ──
    print(f"\n🔵 Lever ({len(LEVER_COMPANIES)} companies)...")
    lv_jobs = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(fetch_lever, t, n): (t,n) for t,n in LEVER_COMPANIES}
        for f in as_completed(futures):
            result = f.result()
            lv_jobs.extend(result)
    print(f"   Found {len(lv_jobs)} matching jobs")
    all_jobs.extend(lv_jobs)

    # ── Ashby ──
    print(f"\n🟣 Ashby ({len(ASHBY_COMPANIES)} companies)...")
    ash_jobs = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(fetch_ashby, t, n): (t,n) for t,n in ASHBY_COMPANIES}
        for f in as_completed(futures):
            result = f.result()
            ash_jobs.extend(result)
    print(f"   Found {len(ash_jobs)} matching jobs")
    all_jobs.extend(ash_jobs)

    # ── Workday ──
    print(f"\n🟠 Workday ({len(WORKDAY_COMPANIES)} companies)...")
    wd_jobs = []
    with ThreadPoolExecutor(max_workers=5) as ex:
        futures = {ex.submit(fetch_workday, url, n): (url,n) for url,n in WORKDAY_COMPANIES}
        for f in as_completed(futures):
            result = f.result()
            wd_jobs.extend(result)
    print(f"   Found {len(wd_jobs)} matching jobs")
    all_jobs.extend(wd_jobs)

    # ── Dedupe + Sort ──
    all_jobs = dedupe(all_jobs)
    all_jobs.sort(key=lambda x: x["score"], reverse=True)

    print(f"\n✅ Total unique matching jobs: {len(all_jobs)}")
    print(f"   Top score: {all_jobs[0]['score'] if all_jobs else 0}")
    print(f"   Companies covered: {len(set(j['company'] for j in all_jobs))}")

    # ── Output ──
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(script_dir, "..", "docs")
    os.makedirs(docs_dir, exist_ok=True)
    output = {
        "jobs": all_jobs[:100],  # top 100
        "total": len(all_jobs),
        "last_updated": datetime.now(timezone.utc).strftime("%B %d, %Y %I:%M %p UTC"),
        "companies_scanned": len(GREENHOUSE_COMPANIES) + len(LEVER_COMPANIES) + len(ASHBY_COMPANIES) + len(WORKDAY_COMPANIES),
        "sources": {
            "greenhouse": len(gh_jobs),
            "lever": len(lv_jobs),
            "ashby": len(ash_jobs),
            "workday": len(wd_jobs),
        }
    }
   with open(os.path.join(docs_dir, "jobs.json"), "w") as f:
        json.dump(output, f, indent=2)
    print(f"   Saved to docs/jobs.json")
    return output


if __name__ == "__main__":
    run_all()
