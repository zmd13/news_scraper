#!/usr/bin/env python3
"""
Healthcare News Scraper
Scrapes RSS feeds for healthcare news and generates a brief
"""
import yaml
from feed_parser import FeedParser
from brief_generator import BriefGenerator


def load_config(config_file: str = "../config.yaml") -> dict:
    """Load configuration from YAML file"""
    import os
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Build path to config file (in parent directory)
    config_path = os.path.join(script_dir, config_file)

    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    """Main function to run the news scraper"""
    print("=" * 70)
    print("HEALTHCARE NEWS SCRAPER")
    print("=" * 70)
    print()

    # Load configuration
    print("Loading configuration...")
    config = load_config()

    industry = config.get('industry', 'Healthcare')
    feeds = config.get('rss_feeds', [])
    keywords = config.get('keywords', [])
    max_articles = config.get('max_articles', 10)
    time_window_hours = config.get('time_window_hours', 24)
    output_format = config.get('output_format', 'markdown')
    output_file = config.get('output_file', 'healthcare_brief.md')

    print(f"Industry: {industry}")
    print(f"RSS Feeds: {len(feeds)}")
    print(f"Keywords: {len(keywords)}")
    print(f"Time Window: {time_window_hours} hours")
    print(f"Max Articles: {max_articles}")
    print()

    # Parse feeds
    print("Parsing RSS feeds...")
    print("-" * 70)
    parser = FeedParser(feeds, keywords, time_window_hours)
    articles = parser.get_top_articles(max_articles)
    print("-" * 70)
    print(f"\nFound {len(articles)} relevant articles")
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
    from datetime import datetime
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
