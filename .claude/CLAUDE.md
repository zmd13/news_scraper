# Healthcare News Scraper

## Current State (Nov 16, 2025)
- ✅ Production-ready Google News scraper (FREE, no API key required)
- ✅ 7-day lookback period, ~50-70 articles per run
- ✅ Fuzzy deduplication (42% duplicate removal rate)
- ✅ 10 natural categories discovered from data
- ✅ Spam filtering (100% effectiveness)
- ✅ Categorized HTML output with table of contents
- 📋 GitHub Issue #1: Auto-run scheduling + email delivery (planned)

## Production Files
```
src/
├── scraper_google.py           # Main production scraper
├── google_news_client.py       # Google News fetcher with deduplication
├── brief_generator.py          # HTML generator with categorization
├── debug/                      # Debug tools (shows duplicates)
│   ├── scraper_google_debug.py
│   └── google_news_client_debug.py
└── archive/                    # Old/unused code (NewsAPI, RSS, etc.)
```

## Run Commands
```bash
# Production scraper (7 days, categorized HTML)
cd /mnt/c/Users/17342/OneDrive/Claude\ Code/Code/news_scraper/briefs
../venv/bin/python ../src/scraper_google.py

# Debug mode (shows duplicates marked in red)
../venv/bin/python ../src/debug/scraper_google_debug.py

# View latest brief
ls -lt healthcare_brief_google_*.html | head -1
```

## Configuration
- **Main config:** `config_google.yaml`
  - Time period: 7 days
  - Search queries: 25 healthcare-specific queries
  - No article limit (shows all unique articles found)
  - Language: English, Country: US

## Categories (Display Order)
1. Industry Analysis
2. Risk Adjustment & Actuarial
3. CMS Rules & Policy
4. Value-Based Care Models
5. Technology & Platforms
6. Provider Contracts & Disputes
7. Medicare Advantage Market
8. M&A and Partnerships
9. ACO Performance
10. Company Earnings & Financial Performance
11. Other (uncategorized)

## Key Features
- **Fuzzy Deduplication:** Jaccard similarity, excludes 26 common healthcare terms
- **Spam Filtering:** Two-stage (bad sources + content-based)
- **Categorization:** Keyword-based, 80-85% accuracy
- **Output:** Professional HTML with clickable TOC

## Expected Results (7-Day Run)
- Total articles: 50-70 unique
- Duplicates removed: ~40-45 (42% rate)
- Categories with articles: 8-10
- "Other" category: 20-40%
- Runtime: 2-3 minutes

## Next Tasks (Issue #1)
- [ ] Implement auto-run scheduling (Windows Task Scheduler / cron)
- [ ] Implement email delivery (SMTP)
- [ ] See: `docs/SCHEDULING_GUIDE.md`
- [ ] See: `docs/FEATURE_REQUEST_EMAIL_DELIVERY.md`

## Important Paths
- **Repository:** https://github.com/zmd13/news_scraper
- **Output:** `briefs/healthcare_brief_google_YYYY-MM-DD.html`
- **Logs:** `logs/scraper_YYYY-MM-DD.log` (planned)
- **Docs:** `docs/` directory

## Virtual Environment
```bash
# Activate venv
cd /mnt/c/Users/17342/OneDrive/Claude\ Code/Code/news_scraper
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Git Workflow
```bash
# Stage changes
git add .

# Commit
git commit -m "Description"

# Push to GitHub
git push origin main
```

## User Profile
- **Role:** Healthcare actuary
- **Focus:** Value-based care, ACOs, Medicare Advantage, risk adjustment
- **Target Companies:** Pearl Health, Vytalize, Agilon, Aledade
- **Competitors:** Milliman, Oliver Wyman, Arbital, Arcadia
- **Output Use:** Daily news digest for industry tracking
