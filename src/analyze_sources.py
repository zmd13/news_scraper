#!/usr/bin/env python3
"""
Source Analysis Script
Analyzes Google News results to evaluate source quality and categorize content
"""
from bs4 import BeautifulSoup
from collections import defaultdict
import re


def analyze_sources(html_file):
    """Analyze sources from Google News HTML brief"""

    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Extract all articles
    articles = []
    article_divs = soup.find_all('div', class_='article')

    for div in article_divs:
        title_tag = div.find('h3')
        meta_tag = div.find('p', class_='meta')

        if title_tag and meta_tag:
            title = title_tag.get_text()
            meta_text = meta_tag.get_text()

            # Extract source from meta
            source_match = re.search(r'Source: ([^|]+)', meta_text)
            source = source_match.group(1).strip() if source_match else 'Unknown'

            articles.append({
                'title': title,
                'source': source
            })

    # Group by source
    sources = defaultdict(list)
    for article in articles:
        sources[article['source']].append(article['title'])

    # Sort sources by article count
    sorted_sources = sorted(sources.items(), key=lambda x: len(x[1]), reverse=True)

    print("=" * 100)
    print(f"SOURCE ANALYSIS - {len(articles)} Total Articles from {len(sources)} Sources")
    print("=" * 100)
    print()

    # Print source summary
    for source, titles in sorted_sources:
        print(f"\n{'=' * 100}")
        print(f"SOURCE: {source}")
        print(f"ARTICLE COUNT: {len(titles)}")
        print(f"{'=' * 100}")

        # Show first 5 titles as samples
        print("\nSample Titles:")
        for i, title in enumerate(titles[:5], 1):
            # Clean up title (remove numbering)
            clean_title = re.sub(r'^\d+\.\s*', '', title)
            print(f"  {i}. {clean_title}")

        if len(titles) > 5:
            print(f"  ... and {len(titles) - 5} more")

    print("\n" + "=" * 100)
    print("ANALYSIS COMPLETE")
    print("=" * 100)
    print(f"\nTotal Articles: {len(articles)}")
    print(f"Total Sources: {len(sources)}")
    print(f"\nTop 10 Sources by Volume:")
    for i, (source, titles) in enumerate(sorted_sources[:10], 1):
        print(f"  {i}. {source}: {len(titles)} articles")


if __name__ == "__main__":
    html_file = "../briefs/healthcare_brief_google_2025-11-16.html"
    analyze_sources(html_file)
