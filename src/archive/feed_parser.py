"""RSS Feed Parser for Healthcare News"""
import feedparser
import requests
from datetime import datetime, timedelta
from dateutil import parser as date_parser
from typing import List, Dict, Optional


class FeedParser:
    """Parses RSS feeds and extracts relevant articles"""

    def __init__(self, feeds: List[Dict[str, str]], keywords: List[str], time_window_hours: int = 24):
        """
        Initialize the feed parser

        Args:
            feeds: List of feed dictionaries with 'name' and 'url'
            keywords: List of keywords to identify relevant articles
            time_window_hours: How far back to look for news (in hours)
        """
        self.feeds = feeds
        self.keywords = [kw.lower() for kw in keywords]
        self.time_window = timedelta(hours=time_window_hours)
        self.cutoff_time = datetime.now() - self.time_window

    def parse_all_feeds(self) -> List[Dict]:
        """
        Parse all configured RSS feeds and return relevant articles

        Returns:
            List of article dictionaries
        """
        all_articles = []

        for feed_info in self.feeds:
            try:
                articles = self._parse_single_feed(feed_info)
                all_articles.extend(articles)
                print(f"✓ Parsed {len(articles)} articles from {feed_info['name']}")
            except Exception as e:
                print(f"✗ Error parsing {feed_info['name']}: {str(e)}")

        # Sort by publication date (newest first)
        all_articles.sort(key=lambda x: x['published'], reverse=True)

        return all_articles

    def _parse_single_feed(self, feed_info: Dict[str, str]) -> List[Dict]:
        """Parse a single RSS feed"""
        articles = []

        # Parse the feed
        feed = feedparser.parse(feed_info['url'])

        for entry in feed.entries:
            # Extract article data
            article = self._extract_article_data(entry, feed_info['name'])

            if article and self._is_relevant(article):
                articles.append(article)

        return articles

    def _extract_article_data(self, entry, source_name: str) -> Optional[Dict]:
        """Extract relevant data from a feed entry"""
        try:
            # Get publication date
            published = None
            if hasattr(entry, 'published'):
                published = date_parser.parse(entry.published)
            elif hasattr(entry, 'updated'):
                published = date_parser.parse(entry.updated)
            else:
                # If no date, skip this article
                return None

            # Remove timezone info for comparison
            published_naive = published.replace(tzinfo=None) if published.tzinfo else published

            # Check if article is within time window
            if published_naive < self.cutoff_time:
                return None

            # Extract description/summary
            description = ""
            if hasattr(entry, 'summary'):
                description = entry.summary
            elif hasattr(entry, 'description'):
                description = entry.description

            # Clean HTML tags from description if present
            from bs4 import BeautifulSoup
            description = BeautifulSoup(description, 'html.parser').get_text()

            article = {
                'title': entry.title if hasattr(entry, 'title') else 'No Title',
                'link': entry.link if hasattr(entry, 'link') else '',
                'description': description.strip(),
                'published': published_naive,
                'source': source_name
            }

            return article

        except Exception as e:
            print(f"  Warning: Could not parse entry: {str(e)}")
            return None

    def _is_relevant(self, article: Dict) -> bool:
        """
        Check if article is relevant based on keywords

        Args:
            article: Article dictionary

        Returns:
            True if article contains any of the keywords
        """
        # Combine title and description for keyword matching
        text = f"{article['title']} {article['description']}".lower()

        # Check if any keyword appears in the text
        for keyword in self.keywords:
            if keyword in text:
                return True

        return False

    def get_top_articles(self, max_articles: int = 10) -> List[Dict]:
        """
        Get the top N most recent relevant articles

        Args:
            max_articles: Maximum number of articles to return

        Returns:
            List of top articles
        """
        all_articles = self.parse_all_feeds()
        return all_articles[:max_articles]
