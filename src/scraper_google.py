#!/usr/bin/env python3
"""
Healthcare News Scraper - Google News Version
Uses Google News RSS to search for healthcare news (FREE, no API key needed)
"""
import yaml
from datetime import datetime
from google_news_client import GoogleNewsFetcher
from brief_generator import BriefGenerator


def load_config(config_file: str = "../config/config_google.yaml") -> dict:
    """Load configuration from YAML file"""
    import os
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Build path to config file
    config_path = os.path.join(script_dir, config_file)

    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    """Main function to run the Google News scraper"""
    print("=" * 70)
    print("HEALTHCARE NEWS SCRAPER - Google News Edition (FREE)")
    print("=" * 70)
    print()

    # Load configuration
    print("Loading configuration...")
    config = load_config()

    industry = config.get('industry', 'Healthcare')
    google_news_config = config.get('google_news', {})
    keywords = config.get('keywords', [])
    max_articles = config.get('max_articles', 20)
    output_format = config.get('output_format', 'html')
    output_file = config.get('output_file', '../briefs/healthcare_brief_google.html')

    # Get Google News settings
    period = google_news_config.get('period', '7d')
    language = google_news_config.get('language', 'en')
    country = google_news_config.get('country', 'US')
    search_queries = google_news_config.get('search_queries', [])
    max_results_per_query = google_news_config.get('max_results_per_query', 50)

    print(f"Industry: {industry}")
    print(f"Search Queries: {len(search_queries)}")
    print(f"Keywords: {len(keywords)}")
    print(f"Time Period: {period}")
    print(f"Language: {language}")
    print(f"Country: {country}")
    print(f"Max Articles: {max_articles}")
    print()

    # Fetch articles from Google News
    print("Fetching articles from Google News RSS...")
    print("-" * 70)

    fetcher = GoogleNewsFetcher(keywords, period, language, country)
    articles = fetcher.search_by_queries(search_queries, max_results_per_query)

    print("-" * 70)
    print(f"Found {len(articles)} total articles from Google News")
    print()

    # Limit to max_articles
    articles = articles[:max_articles]
    print(f"Showing top {len(articles)} articles")
    print()

    # Categorize articles
    print("Categorizing articles...")
    for article in articles:
        article['category'] = fetcher.categorize_article(article)

    # Count by category
    from collections import Counter
    category_counts = Counter(article['category'] for article in articles)
    print("Category breakdown:")
    for category, count in category_counts.most_common():
        print(f"  {category}: {count} articles")
    print()

    # Generate brief
    print("Generating categorized brief...")
    generator = BriefGenerator(industry)

    if output_format == 'markdown':
        brief = generator.generate_markdown_brief(articles)
    elif output_format == 'text':
        brief = generator.generate_text_brief(articles)
    elif output_format == 'html':
        brief = generator.generate_categorized_html_brief(articles)
    else:
        brief = generator.generate_markdown_brief(articles)
        print(f"Warning: Unknown format '{output_format}', using markdown")

    # Replace {date} placeholder in filename
    if '{date}' in output_file:
        output_file = output_file.replace('{date}', datetime.now().strftime('%Y-%m-%d'))

    # Save brief
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(brief)

    print(f"✓ Brief saved to: {output_file}")
    print()
    print("==" * 35)
    print("DONE! Google News scraper completed successfully.")
    print("==" * 35)


if __name__ == "__main__":
    main()
