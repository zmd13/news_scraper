# Healthcare News Scraper - Claude Documentation

## Project Overview
A news scraper focused on value-based care (VBC) and healthcare actuarial topics. Built for a healthcare actuary tracking ACOs, MSSP, Medicare Advantage, and related companies/competitors.

## User Profile
- **Role:** Healthcare actuary
- **Focus:** Value-based care, providers, health systems, IPAs, clinically integrated networks
- **Main Companies Tracked:** Pearl Health, Vytalize, Agilon, UnitedHealth, Aledade, Honest Health, Palm Beach ACO, ACOs in MSSP/ACO REACH
- **Competitors:** Milliman, Oliver Wyman, Arbital, Validate Health, Alliant, Falcon Health, Arcadia, CareJourney
- **Companies to Watch:** Lightbeam, Innovaccer, Health Endeavors, Cedar Gate

## Project Structure
```
news_scraper/
├── .env                        # API keys (gitignored)
├── .env.example               # Template for API keys
├── .gitignore                 # Git ignore rules
├── config.yaml                # RSS + Web scraping config
├── config_newsapi.yaml        # NewsAPI scraper config
├── requirements.txt           # Python dependencies
├── claude.md                  # This file
├── src/
│   ├── scraper.py            # Hybrid RSS + Web scraper (OLD)
│   ├── scraper_newsapi.py    # NewsAPI scraper (NEW - RECOMMENDED)
│   ├── feed_parser.py        # RSS feed parser
│   ├── web_scraper.py        # Web scraping module
│   ├── news_api_client.py    # NewsAPI client
│   └── brief_generator.py    # HTML/Markdown/Text brief generator
├── briefs/                    # Output folder (gitignored)
└── venv/                      # Python virtual env (gitignored)
```

## Two Scrapers Available

### 1. Hybrid Scraper (scraper.py)
**Sources:** RSS feeds + Web scraping
- 8 RSS feeds (Healthcare Dive, Fierce Healthcare, etc.)
- 8 web scrape sources (Milliman, Arbital, Pearl Health, etc.)

**Run:**
```bash
cd src
../venv/bin/python scraper.py
```

**Output:** `briefs/healthcare_brief_{date}.html`

**Pros:** Direct access to specific sources
**Cons:** ~14 articles, some broken feeds

### 2. NewsAPI Scraper (scraper_newsapi.py) - RECOMMENDED
**Sources:** NewsAPI searching 35 healthcare domains
- Industry news: Healthcare Dive, Fierce Healthcare, Modern Healthcare, Becker's, STAT
- Mainstream: WSJ, NYT, Bloomberg, Reuters, CNBC
- Policy: KFF Health News, ProPublica, NPR, The Hill
- Company news: GlobeNewswire, Yahoo Finance

**Run:**
```bash
cd src
../venv/bin/python scraper_newsapi.py
```

**Output:** `briefs/healthcare_brief_newsapi_{date}.html`

**Pros:**
- Broader coverage (35 domains)
- No junk (domain filtering)
- Searches across all news sources
- ~16 quality articles per week

**Cons:**
- Requires NewsAPI key (free tier: 100 requests/day)
- Free tier limited to last 30 days

## Configuration

### Environment Variables (.env)
```bash
NEWSAPI_KEY=your_api_key_here
```

**Important:** Never commit .env to git! It's in .gitignore.

### NewsAPI Config (config_newsapi.yaml)

**Key Settings:**
- `time_window_hours: 168` (7 days)
- `max_articles: 20`
- `domains:` 35 healthcare-focused domains
- `search_queries:` 5 broad queries covering:
  1. Value-based care terms (ACO, MSSP, ACO REACH)
  2. Competitors (Milliman, Oliver Wyman, Arbital, Arcadia)
  3. Companies to watch (Pearl Health, Agilon, Aledade, etc.)
  4. Government/policy (CMS, CMMI, Medicare Advantage)
  5. Financial terms (shared savings, capitation, bundled payments)

**52 Keywords for Filtering:**
- Value-based care models
- Government programs (CMS, CMMI, MSSP, ACO REACH)
- Company names (target companies & competitors)
- Financial/analytics terms (risk adjustment, HCC, RAF score, actuarial)

## Key Topics Tracked

**Value-Based Care:**
- ACO, MSSP, ACO REACH
- Medicare Shared Savings Program
- Capitation, bundled payments
- Two-sided risk, downside risk

**Organizations:**
- Health systems, IPAs, CINs
- Target companies: Pearl Health, Vytalize, Agilon, Aledade
- Competitors: Milliman, Oliver Wyman, Arbital, Arcadia

**Financial/Analytics:**
- Fraud waste and abuse (FWA)
- Risk adjustment, HCC, RAF scores
- Total cost of care, MLR
- Predictive modeling, risk stratification
- Advanced analytics

**Policy:**
- CMS, CMMI
- Medicare Advantage
- Payment reform

## Installation & Setup

### 1. Create Virtual Environment
```bash
cd news_scraper
python3 -m venv venv
```

### 2. Install Dependencies
```bash
./venv/bin/pip install -r requirements.txt
```

**Dependencies:**
- feedparser (RSS parsing)
- requests (HTTP)
- beautifulsoup4 (web scraping)
- python-dateutil (date parsing)
- pyyaml (config files)
- newsapi-python (NewsAPI client)
- python-dotenv (environment variables)

### 3. Get NewsAPI Key
1. Sign up at https://newsapi.org
2. Get your free API key
3. Create `.env` file: `NEWSAPI_KEY=your_key_here`

### 4. Run Scraper
```bash
cd src
../venv/bin/python scraper_newsapi.py
```

## Output Format

**HTML Brief includes:**
- Header with date and article count
- Executive Summary (themes and sources)
- Key Topics (top 5 headlines)
- Detailed News Items (full articles with links)
- Clean, professional styling

**Alternative formats:** Can generate Markdown or plain text by changing `output_format` in config.

## Git Setup

**Files tracked in git:**
- All source code (src/*.py)
- Config files (*.yaml)
- Requirements (requirements.txt)
- Documentation (claude.md, README.md)
- .env.example (template)

**Files NOT in git (.gitignore):**
- .env (API keys)
- briefs/ (generated output)
- venv/ (virtual environment)
- __pycache__/ (Python cache)

**Commit workflow:**
```bash
git add .
git commit -m "Description of changes"
git push
```

## NewsAPI Free Tier Limits

- **100 requests/day**
- **Last 30 days** of articles only
- Our usage: **5 requests per run** (one per search query)
- Can run **20 times per day** within limits

## Known Issues & Limitations

### Current Issues:
1. **Only 16 articles in 7 days** - May need broader queries or longer time window
2. **Some RSS feeds broken** (Modern Healthcare, Becker's, Advisory Board)
3. **Mainstream media (WSJ, NYT) rarely cover VBC topics** - in domain list but rarely show up
4. **60% of articles are GlobeNewswire** - Company press releases dominate results

### Domain Filtering Tradeoffs:
- **With filtering:** Zero junk, but fewer articles
- **Without filtering:** More articles, but 60% junk (CMS Energy, basketball, Python packages)
- **Current approach:** 35-domain whitelist = quality over quantity

## Potential Improvements

### Short-term:
1. **Adjust queries** - Broader or more specific terms
2. **Increase time window** - Try 14 or 30 days
3. **Add Google News RSS** - Free alternative/supplement to NewsAPI
4. **Fix broken RSS feeds** - Find working feed URLs

### Medium-term:
1. **Add prioritization** - Rank articles by relevance/importance
2. **Source diversity** - Balance between news types (policy vs company vs finance)
3. **Deduplication** - Remove similar/duplicate articles
4. **Email delivery** - Auto-send briefs

### Long-term:
1. **Combine all scrapers** - RSS + Web + NewsAPI + Google News
2. **AI summarization** - Use Claude API for better summaries
3. **Trend analysis** - Track topics over time
4. **Alerting** - Notify on specific company/keyword mentions

## Troubleshooting

### "No articles found"
- Check time window (may need longer than 7 days)
- Verify NewsAPI key in .env
- Check if queries are too specific

### "API key error"
- Ensure .env file exists in project root
- Verify NEWSAPI_KEY is set correctly
- Check API key is valid at newsapi.org

### "Import errors"
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

### "Too much junk in results"
- Verify domain filtering is enabled in config_newsapi.yaml
- Check domains list is properly formatted

## Development History

1. **Initial build:** RSS-only scraper with 5 healthcare feeds
2. **Added web scraping:** Direct scraping of company blogs (Milliman, Arbital, etc.)
3. **Added NewsAPI:** Broad search across all news sources
4. **Domain filtering:** Reduced junk from 60% to 0%
5. **Expanded domains:** Added mainstream media (WSJ, NYT, Bloomberg)
6. **Security:** API keys moved to .env file
7. **Current state:** Two scrapers, NewsAPI recommended

## Future Enhancements to Consider

1. **Google News RSS** - Free alternative to NewsAPI
2. **Twitter/LinkedIn monitoring** - Track company social media
3. **Email digests** - Auto-send daily/weekly briefs
4. **Categorization** - Group by topic (policy, company news, finance)
5. **Trend tracking** - Identify hot topics over time
6. **Custom alerts** - Notify on specific keywords/companies
7. **Data export** - CSV/JSON output for analysis
8. **Web interface** - View briefs in browser
9. **Scheduling** - Cron job for automated runs
10. **Multi-user** - Support multiple users with different interests

## Contact & Support

- GitHub: https://github.com/zmd13/news_scraper
- Created: November 2025
- Built with: Claude Code (Anthropic)

---

**Last Updated:** November 15, 2025
