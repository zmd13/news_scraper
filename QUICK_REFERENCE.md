# Healthcare News Scraper - Quick Reference

**Version:** 1.4 Production | **Status:** ✅ Ready for Daily Use

---

## Daily Command

```bash
cd /mnt/c/Users/17342/OneDrive/Claude\ Code/Code/news_scraper/briefs
../venv/bin/python ../src/scraper_google.py
```

**Runtime:** ~2-3 minutes
**Output:** `healthcare_brief_google_2025-MM-DD.html`

---

## Expected Results (7 Days)

| Metric | Expected Range |
|--------|----------------|
| Total Articles | 50-70 |
| Categories with Articles | 6-10 |
| "Other" Category | 20-40% |
| Runtime | 2-3 minutes |

---

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
11. Other

---

## Debug Mode (When Needed)

```bash
cd /mnt/c/Users/17342/OneDrive/Claude\ Code/Code/news_scraper/briefs
../venv/bin/python ../src/scraper_google_debug.py
```

**Use when:** You want to see which articles were flagged as duplicates

---

## Common Issues

### "No module named 'gnews'"
```bash
cd /mnt/c/Users/17342/OneDrive/Claude\ Code/Code/news_scraper
source venv/bin/activate
pip install -r requirements.txt
```

### Too Many "Other" Articles (>40%)
Review `config_google.yaml` and consider adding more specific search queries

### No Articles Found
- Wait 1 hour (possible Google News rate limit)
- Check internet connection
- Verify time period isn't too narrow

---

## Quick Edits

### Change Time Period
**File:** `config_google.yaml` (line 10)
```yaml
period: "7d"  # Options: "24h", "7d", "30d"
```

### Add Search Query
**File:** `config_google.yaml` (line 22-58)
```yaml
search_queries:
  - "your new query here"
```

### Add Keyword
**File:** `config_google.yaml` (line 61-125)
```yaml
keywords:
  - "your new keyword"
```

---

## File Locations

| File | Path |
|------|------|
| Production Scraper | `src/scraper_google.py` |
| Config File | `config_google.yaml` |
| Output Briefs | `briefs/healthcare_brief_google_*.html` |
| Documentation | `PRODUCTION_README.md` |
| Testing Details | `TESTING_DOCUMENTATION.md` |

---

## Support

1. Check `PRODUCTION_README.md` for detailed guide
2. Check `TESTING_DOCUMENTATION.md` for technical details
3. Run debug mode to diagnose issues
4. Review `config_google.yaml` for settings

---

## Quality Checklist (After Each Run)

- [ ] Brief generated successfully
- [ ] 50-70 articles (7-day period)
- [ ] Categories properly distributed
- [ ] No obvious spam articles
- [ ] "Other" category <40%

---

**Last Updated:** November 16, 2025
**Status:** Production Ready ✅
