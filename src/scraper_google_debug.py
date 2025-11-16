#!/usr/bin/env python3
"""
Healthcare News Scraper - Google News DEBUG VERSION
Shows which articles would be filtered as duplicates
"""
import yaml
from datetime import datetime
from google_news_client_debug import GoogleNewsFetcherDebug
from brief_generator import BriefGenerator


def load_config(config_file: str = "../config_google.yaml") -> dict:
    """Load configuration from YAML file"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, config_file)

    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    """Main function to run the Google News DEBUG scraper"""
    print("=" * 70)
    print("HEALTHCARE NEWS SCRAPER - Google News DEBUG MODE")
    print("Shows duplicates marked with [DUPLICATE] but keeps them in output")
    print("=" * 70)
    print()

    # Load configuration
    print("Loading configuration...")
    config = load_config()

    industry = config.get('industry', 'Healthcare')
    google_news_config = config.get('google_news', {})
    keywords = config.get('keywords', [])
    max_articles = config.get('max_articles', 9999)
    output_format = config.get('output_format', 'html')

    # Get Google News settings
    period = google_news_config.get('period', '30d')
    language = google_news_config.get('language', 'en')
    country = google_news_config.get('country', 'US')
    search_queries = google_news_config.get('search_queries', [])
    max_results_per_query = google_news_config.get('max_results_per_query', 50)

    print(f"Industry: {industry}")
    print(f"Search Queries: {len(search_queries)}")
    print(f"Time Period: {period}")
    print()

    # Fetch articles
    print("Fetching articles from Google News (DEBUG MODE)...")
    print("-" * 70)

    fetcher = GoogleNewsFetcherDebug(keywords, period, language, country)
    articles = fetcher.search_by_queries(search_queries, max_results_per_query)

    print("-" * 70)

    unique_count = sum(1 for a in articles if not a.get('is_duplicate', False))
    dup_count = len(articles) - unique_count

    print(f"Total: {len(articles)} articles")
    print(f"  ✓ Unique: {unique_count}")
    print(f"  ✗ Duplicates: {dup_count}")
    print()

    # Generate DEBUG brief with duplicate markers
    print("Generating DEBUG brief...")
    output_file = f"../briefs/healthcare_brief_google_DEBUG_{datetime.now().strftime('%Y-%m-%d')}.html"

    brief = generate_debug_html(articles, industry)

    # Save brief
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(brief)

    print(f"✓ DEBUG brief saved to: {output_file}")
    print()
    print("=" * 70)
    print("DONE! Review the brief to see which articles were marked as duplicates")
    print("=" * 70)


def generate_debug_html(articles, industry):
    """Generate HTML brief with duplicate status visible"""
    html = []

    # Header
    html.append("<!DOCTYPE html>")
    html.append("<html lang='en'>")
    html.append("<head>")
    html.append("<meta charset='UTF-8'>")
    html.append("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
    html.append(f"<title>{industry} News Brief - DEBUG MODE</title>")
    html.append("<style>")
    css = """
body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        .article {
            margin: 20px 0;
            padding: 20px;
            border-left: 4px solid #3498db;
            border-radius: 4px;
        }
        .article.unique {
            background: #f8f9fa;
        }
        .article.duplicate {
            background: #ffe6e6;
            border-left: 4px solid #e74c3c;
            opacity: 0.8;
        }
        .dup-badge {
            display: inline-block;
            background: #e74c3c;
            color: white;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: bold;
            margin-left: 10px;
        }
        .dup-reason {
            color: #c0392b;
            font-size: 0.9em;
            margin-top: 5px;
            font-style: italic;
        }
        .meta {
            color: #7f8c8d;
            font-size: 0.9em;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .summary {
            background: #e8f4f8;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
        }
"""
    html.append(css)
    html.append("</style>")
    html.append("</head>")
    html.append("<body>")
    html.append("<div class='container'>")

    # Title
    html.append(f"<h1>{industry} News Brief - DEBUG MODE</h1>")

    unique_count = sum(1 for a in articles if not a.get('is_duplicate', False))
    dup_count = len(articles) - unique_count

    html.append(f"<p class='meta'>Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>")
    html.append(f"<div class='summary'>")
    html.append(f"<strong>Total Articles:</strong> {len(articles)}<br>")
    html.append(f"<strong>✓ Unique Articles:</strong> {unique_count}<br>")
    html.append(f"<strong>✗ Duplicates Detected:</strong> {dup_count} (marked in red)")
    html.append(f"</div>")

    # Articles
    html.append("<h2>All Articles (Duplicates Marked)</h2>")

    for idx, article in enumerate(articles, 1):
        is_dup = article.get('is_duplicate', False)
        css_class = 'duplicate' if is_dup else 'unique'

        html.append(f"<div class='article {css_class}'>")

        # Title with badge
        title = f"{idx}. {article['title']}"
        if is_dup:
            title += " <span class='dup-badge'>DUPLICATE</span>"
        html.append(f"<h3>{title}</h3>")

        # Meta
        html.append(f"<p class='meta'>Source: {article['source']} | Published: {article['published'].strftime('%b %d, %Y %I:%M %p')}</p>")

        # Duplicate reason if applicable
        if is_dup:
            reason = article.get('duplicate_reason', 'Unknown reason')
            html.append(f"<p class='dup-reason'>Duplicate Reason: {reason}</p>")

            if 'duplicate_keywords' in article:
                keywords = ', '.join(article['duplicate_keywords'])
                html.append(f"<p class='dup-reason'>Matching keywords: {keywords}</p>")

        # Description and link
        html.append(f"<p>{article['description']}</p>")
        html.append(f"<a href='{article['link']}' target='_blank'>Read More →</a>")
        html.append("</div>")

    # Footer
    html.append("<footer style='margin-top: 40px; padding-top: 20px; border-top: 1px solid #ecf0f1; text-align: center; color: #7f8c8d;'>")
    html.append("DEBUG MODE - This brief shows all articles including duplicates")
    html.append("</footer>")

    html.append("</div>")
    html.append("</body>")
    html.append("</html>")

    return "\n".join(html)


if __name__ == "__main__":
    main()
