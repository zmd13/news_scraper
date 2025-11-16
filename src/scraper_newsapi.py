#!/usr/bin/env python3
"""
Healthcare News Scraper - NewsAPI Version
Uses NewsAPI to search for healthcare news across all sources
"""
import yaml
from datetime import datetime
from news_api_client import NewsAPIFetcher, load_api_key
from brief_generator import BriefGenerator


def load_config(config_file: str = "../config_newsapi.yaml") -> dict:
    """Load configuration from YAML file"""
    import os
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Build path to config file (in parent directory)
    config_path = os.path.join(script_dir, config_file)

    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    """Main function to run the NewsAPI scraper"""
    print("=" * 70)
    print("HEALTHCARE NEWS SCRAPER - NewsAPI Edition")
    print("=" * 70)
    print()

    # Load configuration
    print("Loading configuration...")
    config = load_config()

    industry = config.get('industry', 'Healthcare')
    news_api_config = config.get('news_api', {})
    keywords = config.get('keywords', [])
    max_articles = config.get('max_articles', 20)
    time_window_hours = config.get('time_window_hours', 168)
    output_format = config.get('output_format', 'html')
    output_file = config.get('output_file', '../briefs/healthcare_brief_newsapi.html')

    # Get NewsAPI settings
    search_queries = news_api_config.get('search_queries', [])
    max_results_per_query = news_api_config.get('max_results_per_query', 50)
    domains = news_api_config.get('domains')

    print(f"Industry: {industry}")
    print(f"Search Queries: {len(search_queries)}")
    print(f"Keywords: {len(keywords)}")
    print(f"Domains: {len(domains.split(',')) if domains else 'All'}")
    print(f"Time Window: {time_window_hours} hours")
    print(f"Max Articles: {max_articles}")
    print()

    # Load API key
    try:
        api_key = load_api_key()
        print("✓ API key loaded from .env")
    except Exception as e:
        print(f"✗ Error loading API key: {str(e)}")
        print("Make sure NEWSAPI_KEY is set in your .env file")
        return

    print()

    # Fetch articles from NewsAPI
    print("Fetching articles from NewsAPI...")
    print("-" * 70)

    fetcher = NewsAPIFetcher(api_key, keywords, time_window_hours, domains)
    articles = fetcher.search_by_queries(search_queries, max_results_per_query)

    print("-" * 70)
    print(f"Found {len(articles)} total articles from NewsAPI")
    print()

    # Limit to max_articles
    articles = articles[:max_articles]
    print(f"Showing top {len(articles)} articles")
    print()

    # Generate brief
    print("Generating brief...")
    generator = BriefGenerator(industry)

    if output_format == 'markdown':
        brief = generator.generate_markdown_brief(articles)
    elif output_format == 'text':
        brief = generator.generate_text_brief(articles)
    elif output_format == 'html':
        brief = generator.generate_html_brief(articles)
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
    print("=" * 70)
    print("DONE!")
    print("=" * 70)


if __name__ == "__main__":
    main()
