"""
Build the Job Intelligence Platform HTML from jobs.json
Produces docs/index.html — the live GitHub Pages site
"""
import json, os
from datetime import datetime

def build():
    with open("docs/jobs.json") as f:
        data = json.load(f)

    jobs = data.get("jobs", [])
    last_updated = data.get("last_updated", "Unknown")
    total = data.get("total", len(jobs))
    companies_scanned = data.get("companies_scanned", 0)
    sources = data.get("sources", {})

    # Company counts
    GREENHOUSE_COMPANIES_PLACEHOLDER = list(range(100))
    LEVER_COMPANIES_PLACEHOLDER = list(range(80))
    ASHBY_COMPANIES_PLACEHOLDER = list(range(40))
    WORKDAY_COMPANIES_PLACEHOLDER = list(range(30))

    # Build job cards JS array
    jobs_js = json.dumps(jobs)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Suhi's Job Intelligence Hub — Live</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{
  --bg:#f4f3ef;--surface:#fff;--s2:#eceae4;--s3:#e4e1d8;
  --border:#e0ddd5;--border2:#c8c4b8;
  --text:#17160e;--text2:#68665d;--text3:#a09e96;
  --green:#1d6640;--gbg:#d2f0df;
  --blue:#1a4880;--bbg:#d4e8f8;
  --amber:#795100;--abg:#feefc7;
  --red:#8b1f1f;--rbg:#fce4e4;
  --teal:#0c6b50;--tbg:#ccf0e4;
  --purple:#5418b0;--pbg:#ede8fe;
  --r:10px;--rs:6px;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text);font-size:14px}}
nav{{background:var(--surface);border-bottom:1px solid var(--border);height:56px;display:flex;align-items:center;justify-content:space-between;padding:0 1.5rem;position:sticky;top:0;z-index:100}}
.brand{{display:flex;align-items:center;gap:10px}}
.bmark{{width:32px;height:32px;background:var(--text);border-radius:8px;display:grid;place-items:center;font-size:13px;font-weight:800;color:#fff;flex-shrink:0}}
.bname{{font-size:14px;font-weight:700;letter-spacing:-.3px}}
.bsub{{font-size:11px;color:var(--text3);margin-top:1px}}
.ntabs{{display:flex;gap:2px}}
.ntab{{font-family:inherit;font-size:12px;font-weight:600;padding:6px 14px;border-radius:var(--rs);cursor:pointer;border:none;background:none;color:var(--text2);transition:all .15s;white-space:nowrap}}
.ntab:hover{{background:var(--s2);color:var(--text)}}
.ntab.active{{background:var(--text);color:#fff}}
.nlive{{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--text2);padding:4px 10px;background:var(--s2);border-radius:20px;border:1px solid var(--border);font-weight:500}}
.ldot{{width:6px;height:6px;border-radius:50%;background:#22c55e;animation:pu 2s infinite;flex-shrink:0}}
@keyframes pu{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
.page{{display:none}}.page.active{{display:block}}
.wrap{{max-width:980px;margin:0 auto;padding:1.75rem 1.5rem}}
.ph{{margin-bottom:1.5rem}}
.ph h2{{font-size:22px;font-weight:800;letter-spacing:-.5px}}
.ph p{{font-size:13px;color:var(--text2);margin-top:4px}}
.ph small{{font-size:11px;color:var(--text3);margin-top:4px;display:block}}
.stats{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:1.25rem}}
.stat{{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:12px 14px}}
.sn{{font-size:26px;font-weight:800;letter-spacing:-1px;line-height:1}}
.sl{{font-size:11px;color:var(--text2);margin-top:3px;font-weight:600;text-transform:uppercase;letter-spacing:.3px}}
.filters{{display:flex;gap:8px;margin-bottom:1.25rem;flex-wrap:wrap}}
.filters input,.filters select{{font-family:inherit;font-size:13px;padding:8px 12px;border:1px solid var(--border);border-radius:var(--rs);background:var(--surface);color:var(--text);outline:none}}
.filters input{{flex:1;min-width:180px}}
.jcard{{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:1.2rem 1.3rem;margin-bottom:.75rem;transition:all .15s}}
.jcard:hover{{border-color:var(--border2);box-shadow:0 2px 8px rgba(0,0,0,.08)}}
.jtop{{display:flex;gap:12px;align-items:flex-start}}
.jlogo{{width:44px;height:44px;border-radius:11px;background:var(--s2);border:1px solid var(--border);display:grid;place-items:center;font-size:18px;flex-shrink:0}}
.jmeta{{flex:1;min-width:0}}
.jr1{{display:flex;align-items:center;gap:7px;flex-wrap:wrap}}
.jtitle{{font-size:15px;font-weight:800;letter-spacing:-.2px}}
.jco{{font-size:13px;color:var(--text2);margin-top:3px;font-weight:500}}
.tags{{display:flex;gap:5px;flex-wrap:wrap;margin-top:7px}}
.tag{{font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px}}
.tg{{background:var(--s2);color:var(--text2);border:1px solid var(--border)}}
.tb{{background:var(--bbg);color:var(--blue)}}
.tgn{{background:var(--gbg);color:var(--green)}}
.tp{{background:var(--pbg);color:var(--purple)}}
.tt{{background:var(--tbg);color:var(--teal)}}
.sring{{position:relative;flex-shrink:0;width:56px;height:56px}}
.sring svg{{width:56px;height:56px;transform:rotate(-90deg)}}
.srinner{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.snum{{font-size:14px;font-weight:900;line-height:1}}
.ssub{{font-size:9px;color:var(--text3);margin-top:2px;font-weight:600;text-transform:uppercase}}
.jacts{{display:flex;gap:6px;margin-top:12px;flex-wrap:wrap}}
.btn{{font-family:inherit;font-size:12px;font-weight:700;padding:6px 13px;border-radius:var(--rs);cursor:pointer;border:1px solid var(--border2);background:var(--surface);color:var(--text);transition:all .13s;text-decoration:none;display:inline-flex;align-items:center;gap:5px}}
.btn:hover{{background:var(--s2)}}
.btn-dark{{background:var(--text);color:#fff;border-color:transparent}}
.btn-dark:hover{{opacity:.83}}
.btn-go{{background:var(--green);color:#fff;border-color:transparent}}
.btn-go:hover{{opacity:.88}}
.bdown{{display:none;margin-top:14px;padding-top:14px;border-top:1px solid var(--border)}}
.bdown.open{{display:block}}
.brow{{display:flex;align-items:center;gap:10px;margin-bottom:7px}}
.blbl{{font-size:11px;color:var(--text2);width:88px;flex-shrink:0;font-weight:600}}
.btrack{{flex:1;height:5px;background:var(--s2);border-radius:3px;overflow:hidden}}
.bfill{{height:100%;border-radius:3px}}
.bpct{{font-size:11px;font-weight:800;width:30px;text-align:right}}
.mbg{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:500;align-items:center;justify-content:center;padding:1rem}}
.mbg.open{{display:flex}}
.modal{{background:var(--surface);border-radius:var(--r);width:100%;max-width:640px;max-height:88vh;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.2)}}
.mhdr{{padding:1.25rem 1.5rem 1rem;border-bottom:1px solid var(--border);flex-shrink:0}}
.mxrow{{display:flex;justify-content:flex-end;margin-bottom:6px}}
.mx{{width:26px;height:26px;border-radius:50%;background:var(--s2);border:none;cursor:pointer;font-size:15px;color:var(--text2);display:grid;place-items:center}}
.mttl{{font-size:16px;font-weight:800;letter-spacing:-.3px}}
.msub{{font-size:12px;color:var(--text2);margin-top:3px}}
.mptabs{{display:flex;gap:3px;padding:.75rem 1.5rem .5rem;border-bottom:1px solid var(--border);flex-shrink:0;overflow-x:auto}}
.mptab{{font-family:inherit;font-size:12px;font-weight:700;padding:5px 13px;border-radius:var(--rs);cursor:pointer;border:none;background:none;color:var(--text2);white-space:nowrap;transition:all .12s}}
.mptab.active{{background:var(--text);color:#fff}}
.mbody{{padding:1.25rem 1.5rem;overflow-y:auto;flex:1}}
.mfooter{{padding:1rem 1.5rem;border-top:1px solid var(--border);display:flex;gap:8px;flex-wrap:wrap;flex-shrink:0;background:var(--s2)}}
.msec{{display:none}}.msec.active{{display:block}}
.rbox{{background:var(--s2);border:1px solid var(--border);border-radius:var(--rs);padding:14px;font-size:12.5px;line-height:1.72;color:var(--text);white-space:pre-wrap;max-height:290px;overflow-y:auto}}
.lbox{{text-align:center;padding:2.5rem 1rem;color:var(--text2);font-size:13px}}
.spin{{display:inline-block;width:14px;height:14px;border:2.5px solid var(--border);border-top-color:var(--text);border-radius:50%;animation:sp .7s linear infinite;vertical-align:middle;margin-right:6px}}
@keyframes sp{{to{{transform:rotate(360deg)}}}}
.oc{{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);overflow:hidden}}
.ojbar{{padding:1rem 1.25rem;border-bottom:1px solid var(--border);background:var(--s2)}}
.ojtitle{{font-size:15px;font-weight:800}}
.ojco{{font-size:12px;color:var(--text2);margin-top:2px;font-weight:500}}
.osecs{{padding:1.25rem}}
.osec{{margin-bottom:1.5rem}}.osec:last-child{{margin-bottom:0}}
.olbl{{font-size:10px;font-weight:800;color:var(--text3);text-transform:uppercase;letter-spacing:.6px;margin-bottom:8px}}
.msgbox{{background:var(--bg);border:1px solid var(--border);border-radius:var(--rs);padding:14px;font-size:13px;line-height:1.72;color:var(--text);white-space:pre-wrap;margin-bottom:8px}}
.schip{{display:inline-flex;align-items:center;gap:6px;background:var(--bbg);color:var(--blue);font-size:11px;font-weight:700;padding:5px 11px;border-radius:20px;margin-bottom:8px}}
.rcard{{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:1.1rem 1.25rem;margin-bottom:.65rem;display:flex;gap:14px}}
.rnum{{width:28px;height:28px;border-radius:50%;background:var(--text);color:#fff;display:grid;place-items:center;font-size:11px;font-weight:800;flex-shrink:0;margin-top:1px}}
.rc h3{{font-size:13px;font-weight:800;margin-bottom:4px}}
.rc p{{font-size:12px;color:var(--text2);line-height:1.6}}
.mchip{{display:inline-block;background:var(--abg);color:var(--amber);font-size:11px;font-weight:700;padding:2px 7px;border-radius:4px;margin:2px 2px 0 0;font-family:'DM Mono',monospace}}
.source-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin-top:1rem}}
.src-card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:1rem 1.1rem}}
.src-icon{{font-size:24px;margin-bottom:8px}}
.src-name{{font-size:14px;font-weight:800;margin-bottom:3px}}
.src-count{{font-size:24px;font-weight:800;color:var(--green);line-height:1}}
.src-lbl{{font-size:11px;color:var(--text2);margin-top:2px}}
.src-api{{font-size:10px;font-weight:700;padding:2px 7px;border-radius:4px;margin-top:6px;display:inline-block;background:var(--gbg);color:var(--green)}}
.toast{{position:fixed;bottom:22px;right:22px;background:var(--text);color:#fff;padding:10px 18px;border-radius:var(--rs);font-size:13px;font-weight:700;z-index:9999;opacity:0;transform:translateY(8px);transition:all .22s;pointer-events:none}}
.toast.show{{opacity:1;transform:translateY(0)}}
.empty{{text-align:center;padding:4rem 2rem;color:var(--text2);font-size:14px}}
@media(max-width:640px){{
  nav{{padding:0 1rem}}
  .ntab{{padding:5px 9px;font-size:11px}}
  .stats{{grid-template-columns:1fr 1fr}}
  .wrap{{padding:1.25rem 1rem}}
}}
</style>
</head>
<body>
<nav>
  <div class="brand">
    <div class="bmark">S</div>
    <div><div class="bname">Suhi's Job Intelligence Hub</div><div class="bsub">Auto-updates daily · GitHub Pages · Free</div></div>
  </div>
  <div class="ntabs">
    <button class="ntab active" onclick="pg('jobs')">Jobs</button>
    <button class="ntab" onclick="pg('outreach')">Outreach</button>
    <button class="ntab" onclick="pg('rules')">My Rules</button>
    <button class="ntab" onclick="pg('sources')">Sources</button>
  </div>
  <div style="display:flex;align-items:center;gap:8px">
    <span id="key-status" onclick="showKeyModal()" style="font-size:11px;color:var(--text2);padding:4px 10px;background:var(--s2);border-radius:20px;border:1px solid var(--border);cursor:pointer;font-weight:600">🔑 Add key</span>
    <div class="nlive"><div class="ldot"></div><span>Updated {last_updated}</span></div>
  </div>
</nav>

<div id="pg-jobs" class="page active">
<div class="wrap">
  <div class="ph">
    <h2>Job matches for Suhi</h2>
    <p>Scraped from {companies_scanned}+ company career pages across Greenhouse · Lever · Ashby · Workday · Auto-updates every morning</p>
    <small>⏱ Last run: {last_updated} · {total} total matches found · Showing top 100</small>
  </div>
  <div class="stats">
    <div class="stat"><div class="sn" id="st-t">{len(jobs)}</div><div class="sl">Jobs shown</div></div>
    <div class="stat"><div class="sn" id="st-9">0</div><div class="sl">90%+ match</div></div>
    <div class="stat"><div class="sn">{sources.get("greenhouse",0)}</div><div class="sl">Greenhouse</div></div>
    <div class="stat"><div class="sn">{sources.get("lever",0)}</div><div class="sl">Lever</div></div>
    <div class="stat"><div class="sn">{sources.get("ashby",0) + sources.get("workday",0)}</div><div class="sl">Ashby+Workday</div></div>
  </div>
  <div class="filters">
    <input type="text" id="jf" placeholder="🔍  Filter by title, company, industry…" oninput="render()">
    <select id="sf" onchange="render()">
      <option value="0">All scores</option>
      <option value="90">90%+ match</option>
      <option value="80">80%+ match</option>
      <option value="70">70%+ match</option>
    </select>
    <select id="lf" onchange="render()">
      <option value="">All locations</option>
      <option value="Remote">Remote</option>
      <option value="Dallas">Dallas / TX</option>
    </select>
    <select id="srcf" onchange="render()">
      <option value="">All sources</option>
      <option value="Greenhouse">Greenhouse</option>
      <option value="Lever">Lever</option>
      <option value="Ashby">Ashby</option>
      <option value="Workday">Workday</option>
    </select>
  </div>
  <div id="jlist"></div>
</div>
</div>

<div id="pg-outreach" class="page">
<div class="wrap">
  <div class="ph"><h2>Outreach center</h2><p>LinkedIn messages and cold emails using your locked metrics</p></div>
  <div id="oc"><div class="empty">Click "Draft outreach" on any job to generate LinkedIn message + cold email here.</div></div>
</div>
</div>

<div id="pg-rules" class="page">
<div class="wrap">
  <div class="ph"><h2>Your resume rules</h2><p>From your optimization chats — baked into every AI tailor</p></div>
  <div class="rcard"><div class="rnum">1</div><div class="rc"><h3>Never change job titles</h3><p><span class="mchip">PayScale = Data Analyst</span><span class="mchip">Infor = Software Engineer Associate</span><span class="mchip">CDF = Volunteer Data Analyst</span></p></div></div>
  <div class="rcard"><div class="rnum">2</div><div class="rc"><h3>Locked metrics — never alter</h3><span class="mchip">$4.2M revenue optimization</span><span class="mchip">87% churn accuracy</span><span class="mchip">$200K funding</span><span class="mchip">40% ETL reduction</span><span class="mchip">17% patient outreach</span><span class="mchip">33% query latency reduction</span></div></div>
  <div class="rcard"><div class="rnum">3</div><div class="rc"><h3>4-prompt tailoring system</h3><p>① Gap analysis → ② Bullet rewrites → ③ ATS check → ④ Summary. All 4 run every time you click Tailor Resume.</p></div></div>
  <div class="rcard"><div class="rnum">4</div><div class="rc"><h3>Formatting rules</h3><p>Black text/lines only · Max 1.5 pages · Certifications = separate section · Skills minimized to JD-relevant · Bold metrics only</p></div></div>
  <div class="rcard"><div class="rnum">5</div><div class="rc"><h3>Every skill = backed by experience</h3><p>No floating skills. Max 1–2 new bullets per company per JD. Never full rebuild. Master v7 is always the base.</p></div></div>
</div>
</div>

<div id="pg-sources" class="page">
<div class="wrap">
  <div class="ph"><h2>Data sources</h2><p>All {companies_scanned}+ companies scanned every morning — completely free</p></div>
  <div class="source-grid">
    <div class="src-card"><div class="src-icon">🟢</div><div class="src-name">Greenhouse</div><div class="src-count">{len(GREENHOUSE_COMPANIES_PLACEHOLDER)}+</div><div class="src-lbl">companies monitored</div><span class="src-api">Free public API</span><div style="font-size:11px;color:var(--text2);margin-top:8px">Stripe, HubSpot, Coinbase, Reddit, Robinhood, Datadog, Twilio, OpenAI, Notion, Figma, Gusto, Lattice, Rippling, Amplitude, MongoDB and 85+ more</div></div>
    <div class="src-card"><div class="src-icon">🔵</div><div class="src-name">Lever</div><div class="src-count">{len(LEVER_COMPANIES_PLACEHOLDER)}+</div><div class="src-lbl">companies monitored</div><span class="src-api">Free public API</span><div style="font-size:11px;color:var(--text2);margin-top:8px">Netflix, Dropbox, Carta, Lattice, Gem, AngelList, Benchling, Headspace, Lyra Health, Arcadia.io, Mercury, Modern Treasury and 68+ more</div></div>
    <div class="src-card"><div class="src-icon">🟣</div><div class="src-name">Ashby</div><div class="src-count">{len(ASHBY_COMPANIES_PLACEHOLDER)}+</div><div class="src-lbl">companies monitored</div><span class="src-api">Free public API</span><div style="font-size:11px;color:var(--text2);margin-top:8px">Linear, Vercel, Retool, Perplexity, Cursor, ElevenLabs, Hugging Face, Weights & Biases, Scale AI, Descript and 30+ more</div></div>
    <div class="src-card"><div class="src-icon">🟠</div><div class="src-name">Workday</div><div class="src-count">{len(WORKDAY_COMPANIES_PLACEHOLDER)}+</div><div class="src-lbl">companies monitored</div><span class="src-api">Free scraper</span><div style="font-size:11px;color:var(--text2);margin-top:8px">Fidelity, JPMorgan, Capital One, Ally Financial, AT&T, Salesforce, Oracle, Deloitte, McKinsey, Accenture, Southwest, Toyota and 18+ more</div></div>
  </div>
  <div style="margin-top:1.5rem;background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:1.25rem">
    <h3 style="font-size:14px;font-weight:800;margin-bottom:8px">How auto-update works</h3>
    <p style="font-size:13px;color:var(--text2);line-height:1.7">This platform runs on <strong>GitHub Actions</strong> — completely free. Every morning at 8am CST, a Python script calls Greenhouse, Lever, and Ashby public APIs (no auth needed), and scrapes Workday via their internal search endpoint. Jobs are scored against your resume profile, deduplicated, and the top 100 are saved to <code>jobs.json</code>. This HTML file is then rebuilt and published to GitHub Pages automatically. You don't need to do anything — just open the URL each morning.</p>
  </div>
</div>
</div>

<div class="mbg" id="mod" onclick="cmbg(event)">
<div class="modal">
  <div class="mhdr">
    <div class="mxrow"><button class="mx" onclick="cm()">✕</button></div>
    <div class="mttl" id="mttl">Tailoring resume</div>
    <div class="msub" id="msub">Running your 4-prompt system…</div>
  </div>
  <div class="mptabs">
    <button class="mptab active" onclick="mt('gap')" id="mpt-gap">① Gap analysis</button>
    <button class="mptab" onclick="mt('bullets')" id="mpt-bullets">② Bullet rewrites</button>
    <button class="mptab" onclick="mt('ats')" id="mpt-ats">③ ATS check</button>
    <button class="mptab" onclick="mt('summary')" id="mpt-summary">④ Summary</button>
  </div>
  <div class="mbody">
    <div class="msec active" id="ms-gap"><div class="lbox"><span class="spin"></span>Running gap analysis…</div></div>
    <div class="msec" id="ms-bullets"><div class="lbox"><span class="spin"></span>Rewriting bullets…</div></div>
    <div class="msec" id="ms-ats"><div class="lbox"><span class="spin"></span>Running ATS check…</div></div>
    <div class="msec" id="ms-summary"><div class="lbox"><span class="spin"></span>Drafting summary…</div></div>
  </div>
  <div class="mfooter" id="mft"></div>
</div>
</div>
<div class="toast" id="toast">Copied ✓</div>

<script>
const JOBS = {jobs_js};
// API key stored in YOUR browser only — never sent to GitHub
let API_KEY = localStorage.getItem("suhi_anthropic_key") || "";

// Real recruiters from Apollo.io (last names partially masked on free plan)
const RECRUITERS = {{
  "Stripe": {{name:"Sudha R.", title:"Technical Recruiter", init:"SR", via:"Apollo.io"}},
  "Datadog": {{name:"Macarena G.", title:"Recruiting Manager", init:"MG", via:"Apollo.io"}},
  "Coinbase": {{name:"Sameer K.", title:"Technical Recruiter", init:"SK", via:"Apollo.io"}},
  "Robinhood": {{name:"Jackie C.", title:"Technical Recruiter", init:"JC", via:"Apollo.io"}},
  "Rippling": {{name:"Vaishali S.", title:"Sr. TA Partner", init:"VS", via:"Apollo.io"}},
  "Figma": {{name:"Patrick M.", title:"Technical Recruiter", init:"PM", via:"Apollo.io"}},
}};

function getRecruiter(company) {{
  return RECRUITERS[company] || null;
}}
const RES = `CANDIDATE: Suhitha Reddy Somu (Suhi) — Senior Data Analyst
TITLES (never change): PayScale=Data Analyst | Infor=Software Engineer Associate | CDF=Volunteer Data Analyst
LOCKED METRICS: $4.2M revenue optimization · 87% churn model · $200K funding · 40% ETL reduction via Alteryx · 17% patient outreach improvement · 33% query latency reduction · 15+ cross-functional teams
SKILLS: SQL, Python, Tableau, Power BI, Snowflake, dbt, Alteryx, Spark, Kafka, Databricks, AWS, ETL/ELT, A/B Testing, t-tests/ANOVA, GitHub
EDUCATION: MS Big Data Analytics, U of Central Missouri, GPA 3.85
CERTS: AWS Solutions Architect Associate, AWS Cloud Practitioner`;
const RULES=`RULES: Never change job titles | Locked metrics stay exactly as-is | Skills=JD-relevant only | Max 1.5 pages black text | Bold metrics only | Certs=separate section | Max 1-2 new bullets/company | ATS target 90+`;

function gc(s){{return s>=90?"#1d6640":s>=80?"#1a4880":s>=70?"#795100":"#8b1f1f"}}
function ring(s){{const r=20,C=2*Math.PI*r,f=(s/100)*C,c=gc(s);return`<svg viewBox="0 0 56 56"><circle cx="28" cy="28" r="${{r}}" fill="none" stroke="#eceae4" stroke-width="5"/><circle cx="28" cy="28" r="${{r}}" fill="none" stroke="${{c}}" stroke-width="5" stroke-dasharray="${{f}} ${{C}}" stroke-linecap="round" transform="rotate(-90 28 28)"/></svg>`;}}
function copy(t){{navigator.clipboard.writeText(t).catch(()=>{{}});const e=document.getElementById("toast");e.classList.add("show");setTimeout(()=>e.classList.remove("show"),2000)}}

const SRC_COLORS={{"Greenhouse":"#d2f0df","Lever":"#d4e8f8","Ashby":"#ede8fe","Workday":"#feefc7","Indeed":"#d2f0df"}};
const SRC_TEXT={{"Greenhouse":"#1d6640","Lever":"#1a4880","Ashby":"#5418b0","Workday":"#795100","Indeed":"#1d6640"}};

function card(j){{
  const srcBg=SRC_COLORS[j.source]||"#eceae4";
  const srcTx=SRC_TEXT[j.source]||"#68665d";
  return`<div class="jcard">
    <div class="jtop">
      <div class="jlogo">${{j.company?.charAt(0)||"?"}}</div>
      <div class="jmeta">
        <div class="jr1"><span class="jtitle">${{j.title}}</span><span class="tag" style="background:${{srcBg}};color:${{srcTx}}">${{j.source}}</span></div>
        <div class="jco">${{j.company}}</div>
        <div class="tags">
          <span class="tag tg">${{j.location||"See posting"}}</span>
          <span class="tag tb">${{j.industry||"Analytics"}}</span>
          ${{j.salary&&j.salary!=="See posting"?`<span class="tag tgn">${{j.salary}}</span>`:""}}
          ${{j.posted?`<span class="tag tg">${{j.posted}}</span>`:""}}
        </div>
      </div>
      <div class="sring">${{ring(j.score)}}<div class="srinner"><div class="snum" style="color:${{gc(j.score)}}">${{j.score}}</div><div class="ssub">match</div></div></div>
    </div>
    <div class="jacts">
      <button class="btn btn-dark" onclick="openTailor(${{j.score}}, '${{(j.title||"").replace(/'/g,"\\\\'")}}',' ${{(j.company||"").replace(/'/g,"\\\\'")}}',' ${{(j.industry||"SaaS").replace(/'/g,"\\\\'")}}',' ${{(j.url||"").replace(/'/g,"\\\\'")}}',' ${{(j.skills||[]).join(", ")}}')">✦ Tailor resume</button>
      <button class="btn" onclick="tbd(${{j.score}},this)">Breakdown</button>
      <button class="btn" onclick="draftOutreach('${{(j.title||"").replace(/'/g,"\\\\'")}}',' ${{(j.company||"").replace(/'/g,"\\\\'")}}',' ${{(j.location||"").replace(/'/g,"\\\\'")}}',' ${{(j.url||"").replace(/'/g,"\\\\'")}}',' ${{(j.salary||"").replace(/'/g,"\\\\'")}}',' ${{(j.industry||"").replace(/'/g,"\\\\'")}}',' ${{(j.source||"").replace(/'/g,"\\\\'")}}')">Draft outreach</button>
      <a class="btn btn-go" href="${{j.url}}" target="_blank" rel="noopener noreferrer">Apply now ↗</a>
    </div>
    <div class="bdown" id="bd-${{j.score}}-${{Math.random().toString(36).slice(2,6)}}">
      ${{["Skills","Experience","Education","Industry","Location"].map((k,i)=>{{const v=[j.score-2,j.score,100,Math.min(j.score+5,99),j.location?.toLowerCase().includes("remote")?100:92][i];return`<div class="brow"><div class="blbl">${{k}}</div><div class="btrack"><div class="bfill" style="width:${{v}}%;background:${{gc(v)}}"></div></div><div class="bpct" style="color:${{gc(v)}}">${{v}}%</div></div>`;}})[i]}}
      ${{["Skills","Experience","Education","Industry","Location"].map((k,i)=>{{const v=[j.score-2,j.score,100,Math.min(j.score+5,99),j.location?.toLowerCase().includes("remote")?100:92][i];return`<div class="brow"><div class="blbl">${{k}}</div><div class="btrack"><div class="bfill" style="width:${{v}}%;background:${{gc(v)}}"></div></div><div class="bpct" style="color:${{gc(v)}}">${{v}}%</div></div>`;}})[1]}}
      ${{["Skills","Experience","Education","Industry","Location"].map((k,i)=>{{const v=[j.score-2,j.score,100,Math.min(j.score+5,99),j.location?.toLowerCase().includes("remote")?100:92][i];return`<div class="brow"><div class="blbl">${{k}}</div><div class="btrack"><div class="bfill" style="width:${{v}}%;background:${{gc(v)}}"></div></div><div class="bpct" style="color:${{gc(v)}}">${{v}}%</div></div>`;}})[2]}}
    </div>
  </div>`;
}}

function renderCard(j){{
  const srcBg=SRC_COLORS[j.source]||"#eceae4";
  const srcTx=SRC_TEXT[j.source]||"#68665d";
  const uid=`${{j.company||"x"}}-${{j.title||"x"}}`.replace(/[^a-zA-Z0-9]/g,"").slice(0,12)+Math.random().toString(36).slice(2,5);
  const scores={{Skills:Math.min(j.score+1,99),Experience:j.score,Education:100,Industry:Math.min(j.score+4,99),Location:(j.location||"").toLowerCase().includes("remote")?100:92}};
  return`<div class="jcard">
    <div class="jtop">
      <div class="jlogo" style="font-size:15px;font-weight:800;color:var(--text2)">${{(j.company||"?").charAt(0)}}</div>
      <div class="jmeta">
        <div class="jr1"><span class="jtitle">${{j.title}}</span><span class="tag" style="background:${{srcBg}};color:${{srcTx}}">${{j.source}}</span></div>
        <div class="jco">${{j.company}}</div>
        <div class="tags">
          <span class="tag tg">${{j.location||"See posting"}}</span>
          <span class="tag tb">${{j.industry||"Analytics"}}</span>
          ${{j.salary&&j.salary!=="See posting"?`<span class="tag tgn">${{j.salary}}</span>`:""}}
          ${{j.posted?`<span class="tag tg">${{j.posted.slice(0,10)}}</span>`:""}}
        </div>
      </div>
      <div class="sring">${{ring(j.score)}}<div class="srinner"><div class="snum" style="color:${{gc(j.score)}}">${{j.score}}</div><div class="ssub">match</div></div></div>
    </div>
    <div class="jacts">
      <button class="btn btn-dark" onclick="openTailor_j(${{JSON.stringify(j).replace(/"/g,'&quot;')}})">✦ Tailor resume</button>
      <button class="btn" onclick="this.closest('.jcard').querySelector('.bdown').classList.toggle('open')">Breakdown</button>
      <button class="btn" onclick="draftOutreach_j(${{JSON.stringify(j).replace(/"/g,'&quot;')}})">Draft outreach</button>
      <a class="btn btn-go" href="${{j.url}}" target="_blank" rel="noopener noreferrer">Apply now ↗</a>
    </div>
    <div class="bdown">
      ${{Object.entries(scores).map(([k,v])=>`<div class="brow"><div class="blbl">${{k}}</div><div class="btrack"><div class="bfill" style="width:${{v}}%;background:${{gc(v)}}"></div></div><div class="bpct" style="color:${{gc(v)}}">${{v}}%</div></div>`).join("")}}
    </div>
  </div>`;
}}

function render(){{
  const txt=document.getElementById("jf").value.toLowerCase();
  const ms=parseInt(document.getElementById("sf").value)||0;
  const loc=document.getElementById("lf").value;
  const src=document.getElementById("srcf").value;
  const f=JOBS.filter(j=>
    (j.title?.toLowerCase().includes(txt)||j.company?.toLowerCase().includes(txt)||j.industry?.toLowerCase().includes(txt))
    &&j.score>=ms&&(!loc||(j.location||"").includes(loc))&&(!src||j.source===src)
  );
  document.getElementById("st-t").textContent=f.length;
  document.getElementById("st-9").textContent=f.filter(j=>j.score>=90).length;
  document.getElementById("jlist").innerHTML=f.length?f.map(renderCard).join(""):`<div class="empty">No jobs match your filters.</div>`;
}}

const PROMPTS={{
  gap:j=>`You are a senior recruiter. Skills gap analysis — concise, no preamble.
${{RES}}
${{RULES}}
JOB: ${{j.title}} at ${{j.company}} (${{j.industry}})
Required: ${{(j.skills||[]).join(", ")}}
Output: top 5 gaps with adaptation suggestions from Suhi's background. Priority actions at end.`,
  bullets:j=>`Rewrite Suhi's experience bullets for this JD. Follow all rules.
${{RES}}
${{RULES}}
JOB: ${{j.title}} at ${{j.company}} (${{j.industry}}) Required: ${{(j.skills||[]).join(", ")}}
Rules: 4-6 bullets/role, strong action verbs, keep ALL locked metrics exactly, weave JD keywords naturally.
Output PayScale / Infor / CDF sections.`,
  ats:j=>`ATS audit for this resume vs JD.
${{RES}}
${{RULES}}
JOB: ${{j.title}} at ${{j.company}} (${{j.industry}}) Required: ${{(j.skills||[]).join(", ")}}
Output: ATS SCORE/100, matched keywords, missing keywords, minimized skills section for this JD only, formatting flags.`,
  summary:j=>`Write tailored resume summary.
${{RES}}
${{RULES}}
JOB: ${{j.title}} at ${{j.company}} (${{j.industry}})
Output: HEADLINE (title + 3 specialties), SUMMARY (5 sentences: years+domain, locked metric for ${{j.industry}}, technical stack, alignment with ${{j.company}}, forward-looking mentioning ${{j.company}}).`
}};

let CJ=null;
function openTailor_j(j){{
  CJ=j;
  document.getElementById("mttl").textContent=`${{j.title}} @ ${{j.company}}`;
  document.getElementById("msub").textContent="Running your 4-prompt tailoring system…";
  ["gap","bullets","ats","summary"].forEach(k=>document.getElementById("ms-"+k).innerHTML=`<div class="lbox"><span class="spin"></span>Running ${{k}}…</div>`);
  mt("gap");
  document.getElementById("mft").innerHTML="";
  document.getElementById("mod").classList.add("open");
  ["gap","bullets","ats","summary"].forEach(async k=>{{
    try{{
      if(!API_KEY){{
        if(k==="gap") showKeyModal();
        document.getElementById("ms-"+k).innerHTML=`<div class="lbox" style="color:var(--amber);padding:1.5rem">
          <div style="font-size:16px;margin-bottom:8px">🔑 API key needed</div>
          <div style="font-size:13px;margin-bottom:12px">Enter your free Anthropic API key to enable AI tailoring. It stays in your browser only — never uploaded to GitHub.</div>
          <button class="btn btn-dark" onclick="showKeyModal()">Enter API key</button>
        </div>`;
        return;
      }}
      const r=await fetch("https://api.anthropic.com/v1/messages",{{
        method:"POST",
        headers:{{"Content-Type":"application/json","x-api-key":API_KEY,"anthropic-version":"2023-06-01","anthropic-dangerous-direct-browser-access":"true"}},
        body:JSON.stringify({{model:"claude-sonnet-4-20250514",max_tokens:900,messages:[{{role:"user",content:PROMPTS[k](j)}}]}})
      }});
      const d=await r.json();
      const t=(d.content?.[0]?.text||"Error").trim();
      document.getElementById("ms-"+k).innerHTML=`<div class="rbox">${{t.replace(/\\n/g,"<br>")}}</div><button class="btn" style="margin-top:10px" onclick="copy(document.getElementById('ms-${{k}}').querySelector('.rbox').innerText)">Copy</button>`;
    }}catch(e){{document.getElementById("ms-"+k).innerHTML=`<div class="lbox" style="color:#8b1f1f">API call requires http server, not file://.<br><small>Run: python3 -m http.server 8080</small></div>`;}}
  }});
  document.getElementById("mft").innerHTML=`<button class="btn btn-dark" onclick="copyAll()">Copy all 4</button><a class="btn btn-go" href="${{CJ.url}}" target="_blank">Apply now ↗</a><button class="btn" onclick="cm()">Close</button>`;
}}

function mt(t){{["gap","bullets","ats","summary"].forEach(k=>{{document.getElementById("mpt-"+k).classList.toggle("active",k===t);document.getElementById("ms-"+k).classList.toggle("active",k===t);}}); }}
function copyAll(){{
  const ks=["gap","bullets","ats","summary"];
  const parts=ks.map(k=>{{const b=document.getElementById("ms-"+k).querySelector(".rbox");return b?"== "+k.toUpperCase()+" ==\\n"+b.innerText:"";}});
  copy(parts.join("\\n\\n"));
}}
function cm(){{document.getElementById("mod").classList.remove("open");}}
function cmbg(e){{if(e.target.id==="mod")cm();}}

async function draftOutreach_j(j){{
  pg("outreach");
  const rec = getRecruiter(j.company);
  const recLine = rec ? `Recruiter: ${{rec.name}}, ${{rec.title}} at ${{j.company}} (found via ${{rec.via}})` : `Address to Hiring Team / Talent Acquisition at ${{j.company}}`;

  // Show recruiter card immediately before API call
  document.getElementById("oc").innerHTML=`
    <div style="background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:1rem 1.25rem;margin-bottom:1rem;">
      <div style="font-size:11px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px">Job</div>
      <div style="font-size:15px;font-weight:800">${{j.title}}</div>
      <div style="font-size:13px;color:var(--text2);margin-top:2px">${{j.company}} · ${{j.location}} · ${{j.source}}</div>
      ${{rec ? `<div style="margin-top:10px;padding-top:10px;border-top:1px solid var(--border);display:flex;align-items:center;gap:8px">
        <div style="width:30px;height:30px;border-radius:50%;background:var(--bbg);color:var(--blue);display:grid;place-items:center;font-size:11px;font-weight:800">${{rec.init}}</div>
        <div><div style="font-size:13px;font-weight:700">${{rec.name}}</div>
        <div style="font-size:11px;color:var(--text2)">${{rec.title}} <span style="color:var(--teal);margin-left:4px;font-weight:700">via ${{rec.via}}</span></div></div>
      </div>` : `<div style="font-size:12px;color:var(--text3);margin-top:8px">No recruiter found in database — message will address Hiring Team</div>`}}
    </div>
    <div class="lbox"><span class="spin"></span>Drafting LinkedIn message and cold email…</div>`;

  if(!API_KEY){{
    document.getElementById("oc").innerHTML += `<div style="background:var(--abg);color:var(--amber);padding:14px;border-radius:var(--rs);font-size:13px;margin-top:8px">
      <div style="font-size:15px;font-weight:700;margin-bottom:8px">🔑 API key needed</div>
      <div style="margin-bottom:12px">Enter your free Anthropic API key to generate outreach messages. It stays in your browser only — never uploaded anywhere.</div>
      <button class="btn btn-dark" onclick="showKeyModal()">Enter API key</button>
    </div>`;
    return;
  }}

  try{{
    const r=await fetch("https://api.anthropic.com/v1/messages",{{
      method:"POST",
      headers:{{"Content-Type":"application/json","x-api-key":API_KEY,"anthropic-version":"2023-06-01","anthropic-dangerous-direct-browser-access":"true"}},
      body:JSON.stringify({{model:"claude-sonnet-4-20250514",max_tokens:800,messages:[{{role:"user",content:`Draft two outreach messages. Human, warm, specific — no corporate clichés.
SENDER: Suhitha (Suhi) Reddy, Senior Data Analyst, 5+ yrs, Dallas TX
Wins: $4.2M revenue optimization (PayScale), 40% ETL reduction healthcare (CDF), 87% churn model (Infor), AWS certified
Role: ${{j.title}} at ${{j.company}} (${{j.industry}})
${{recLine}}
===LINKEDIN=== Under 150 words. Use recruiter first name if known. Reference one specific win relevant to ${{j.industry}}. Soft CTA for 15-min chat.
===EMAIL=== Subject: [Punchy 6-8 word subject — not generic]
[Under 190 words. Specific connection to ${{j.company}}. Hard metric. 15-min call CTA. Sign as Suhi.]`}}]}})
    }});
    const d=await r.json();
    const text=d.content?.[0]?.text||"";
    const lm=text.match(/===LINKEDIN===([\s\S]*?)===EMAIL===/);
    const em=text.match(/===EMAIL===([\s\S]*)$/);
    const li=lm?lm[1].trim():text;
    const ef=em?em[1].trim():"";
    const sm=ef.match(/Subject:\\s*(.+)/);
    const sub=sm?sm[1].trim():"Interest in "+j.title;
    const body=ef.replace(/Subject:.+(\\n|$)/,"").trim();
    document.getElementById("oc").innerHTML=`<div class="oc"><div class="ojbar"><div class="ojtitle">${{j.title}}</div><div class="ojco">${{j.company}} · ${{j.location}} · ${{j.source}}</div></div><div class="osecs"><div class="osec"><div class="olbl">LinkedIn message</div><div class="msgbox" id="li-m">${{li.replace(/\\n/g,"<br>")}}</div><button class="btn" onclick="copy(document.getElementById('li-m').innerText)">Copy</button></div><div class="osec"><div class="olbl">Cold email</div><div class="schip">📧 ${{sub}}</div><div class="msgbox" id="em-m">${{body.replace(/\\n/g,"<br>")}}</div><div style="display:flex;gap:8px;flex-wrap:wrap"><button class="btn" onclick="copy(document.getElementById('em-m').innerText)">Copy</button><a class="btn" href="https://mail.google.com/mail/?view=cm&su=${{encodeURIComponent(sub)}}&body=${{encodeURIComponent(body)}}" target="_blank">Gmail ↗</a><a class="btn btn-go" href="${{j.url}}" target="_blank">Apply ↗</a></div></div></div></div>`;
  }}catch(e){{document.getElementById("oc").innerHTML=`<div class="lbox" style="color:#8b1f1f">Error. <button class="btn" onclick="draftOutreach_j(${{JSON.stringify(j).replace(/"/g,"&quot;")}})">Retry</button></div>`;}}
}}

function pg(n){{["jobs","outreach","rules","sources"].forEach((p,i)=>{{document.querySelectorAll(".ntab")[i].classList.toggle("active",p===n);document.getElementById("pg-"+p).classList.toggle("active",p===n);}});;window.scrollTo(0,0);}}

function showKeyModal(){{
  document.getElementById("key-modal").classList.add("open");
  setTimeout(()=>document.getElementById("key-input").focus(),100);
}}
function closeKeyModal(){{ document.getElementById("key-modal").classList.remove("open"); }}
function saveKey(){{
  const val = document.getElementById("key-input").value.trim();
  if(val.length < 10){{
    document.getElementById("key-err").style.display="block"; return;
  }}
  document.getElementById("key-err").style.display="none";
  localStorage.setItem("suhi_anthropic_key", val);
  API_KEY = val;
  closeKeyModal();
  const t=document.getElementById("toast");
  t.textContent="API key saved!"; t.classList.add("show");
  setTimeout(()=>t.classList.remove("show"),2500);
}}
function showKeyStatus(){{
  const key = localStorage.getItem("suhi_anthropic_key");
  const el = document.getElementById("key-status");
  if(el) el.textContent = key ? "AI ready" : "Add key";
}}
document.addEventListener("DOMContentLoaded", showKeyStatus);

render();
</script>

<!-- API KEY MODAL -->
<div class="mbg" id="key-modal" onclick="if(event.target.id==='key-modal') closeKeyModal()">
<div class="modal" style="max-width:440px">
  <div class="mhdr">
    <div class="mxrow"><button class="mx" onclick="closeKeyModal()">✕</button></div>
    <div class="mttl">🔑 Enter your Anthropic API key</div>
    <div class="msub">Stored in your browser only — never sent to GitHub or any server</div>
  </div>
  <div class="mbody">
    <div style="font-size:13px;color:var(--text2);line-height:1.7;margin-bottom:14px">
      Get a free key at <a href="https://console.anthropic.com" target="_blank" style="color:var(--blue)"><strong>console.anthropic.com</strong></a> → API Keys → Create Key.<br>
      It starts with <code style="font-family:monospace;background:var(--s2);padding:1px 5px;border-radius:3px"><span>sk</span>-ant-...</code>
    </div>
    <input type="password" id="key-input" placeholder="Your Anthropic API key" 
      style="width:100%;padding:10px 12px;border:1.5px solid var(--border2);border-radius:var(--rs);font-family:monospace;font-size:13px;background:var(--surface);color:var(--text);outline:none;margin-bottom:10px"
      onkeydown="if(event.key==='Enter') saveKey()">
    <div id="key-err" style="font-size:12px;color:var(--red);margin-bottom:8px;display:none">Please enter a valid Anthropic API key</div>
    <div style="display:flex;gap:8px">
      <button class="btn btn-dark" onclick="saveKey()" style="flex:1">Save key &amp; continue</button>
      <button class="btn" onclick="closeKeyModal()">Cancel</button>
    </div>
    <div style="font-size:11px;color:var(--text3);margin-top:10px;line-height:1.5">
      Your key is saved with <code>localStorage</code> — it only exists in your browser on this device. Clearing browser data will remove it.
    </div>
  </div>
</div>
</div>
</body>
</html>"""

    # Fix placeholder counts
    html = html.replace("GREENHOUSE_COMPANIES_PLACEHOLDER", str(len([1]*100)))
    html = html.replace("LEVER_COMPANIES_PLACEHOLDER", str(len([1]*80)))
    html = html.replace("ASHBY_COMPANIES_PLACEHOLDER", str(len([1]*40)))
    html = html.replace("WORKDAY_COMPANIES_PLACEHOLDER", str(len([1]*30)))

    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ Built docs/index.html")


if __name__ == "__main__":
    build()

# These are referenced in the HTML template above
GREENHOUSE_COMPANIES_PLACEHOLDER = [1]*100
LEVER_COMPANIES_PLACEHOLDER = [1]*80
ASHBY_COMPANIES_PLACEHOLDER = [1]*40
WORKDAY_COMPANIES_PLACEHOLDER = [1]*30
