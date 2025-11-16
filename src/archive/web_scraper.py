"""Web Scraper for sites without RSS feeds"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser as date_parser
from typing import List, Dict, Optional
import re


class WebScraper:
    """Scrapes news from websites without RSS feeds"""

    def __init__(self, sources: List[Dict], keywords: List[str], time_window_hours: int = 24):
        """
        Initialize the web scraper

        Args:
            sources: List of source dictionaries with 'name', 'url', and 'type'
            keywords: List of keywords to identify relevant articles
            time_window_hours: How far back to look for news (in hours)
        """
        self.sources = sources
        self.keywords = [kw.lower() for kw in keywords]
        self.time_window = timedelta(hours=time_window_hours)
        self.cutoff_time = datetime.now() - self.time_window
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape_all_sources(self) -> List[Dict]:
        """
        Scrape all configured web sources

        Returns:
            List of article dictionaries
        """
        all_articles = []

        for source_info in self.sources:
            try:
                articles = self._scrape_single_source(source_info)
                all_articles.extend(articles)
                print(f"✓ Scraped {len(articles)} articles from {source_info['name']}")
            except Exception as e:
                print(f"✗ Error scraping {source_info['name']}: {str(e)}")

        # Sort by publication date (newest first)
        all_articles.sort(key=lambda x: x.get('published', datetime.min), reverse=True)

        return all_articles

    def _scrape_single_source(self, source_info: Dict) -> List[Dict]:
        """Scrape a single web source"""
        articles = []

        try:
            response = self.session.get(source_info['url'], timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Try different scraping strategies based on source type
            if source_info['type'] == 'blog':
                articles = self._scrape_blog_page(soup, source_info)
            elif source_info['type'] == 'news_list':
                articles = self._scrape_news_list(soup, source_info)
            elif source_info['type'] == 'resources':
                articles = self._scrape_resources_page(soup, source_info)
            else:
                articles = self._scrape_generic(soup, source_info)

        except Exception as e:
            print(f"  Warning: Could not scrape {source_info['name']}: {str(e)}")

        return articles

    def _scrape_blog_page(self, soup: BeautifulSoup, source_info: Dict) -> List[Dict]:
        """Scrape a blog-style page"""
        articles = []

        # Common blog post selectors
        selectors = [
            'article',
            '.post',
            '.blog-post',
            '.entry',
            '[class*="post-"]',
            '[class*="article"]'
        ]

        posts = []
        for selector in selectors:
            posts = soup.select(selector)
            if posts:
                break

        for post in posts[:20]:  # Limit to 20 most recent
            article = self._extract_article_from_element(post, source_info)
            if article and self._is_relevant(article):
                articles.append(article)

        return articles

    def _scrape_news_list(self, soup: BeautifulSoup, source_info: Dict) -> List[Dict]:
        """Scrape a news list page"""
        articles = []

        # Common news list selectors
        selectors = [
            'article',
            '.news-item',
            '.press-release',
            '.insight-item',
            '[class*="news"]',
            '[class*="insight"]',
            'li a[href]'
        ]

        items = []
        for selector in selectors:
            items = soup.select(selector)
            if items:
                break

        for item in items[:20]:
            article = self._extract_article_from_element(item, source_info)
            if article and self._is_relevant(article):
                articles.append(article)

        return articles

    def _scrape_resources_page(self, soup: BeautifulSoup, source_info: Dict) -> List[Dict]:
        """Scrape a resources/content library page"""
        return self._scrape_news_list(soup, source_info)

    def _scrape_generic(self, soup: BeautifulSoup, source_info: Dict) -> List[Dict]:
        """Generic scraping fallback"""
        return self._scrape_blog_page(soup, source_info)

    def _extract_article_from_element(self, element, source_info: Dict) -> Optional[Dict]:
        """Extract article data from a BeautifulSoup element"""
        try:
            # Find title
            title_elem = (
                element.find('h1') or
                element.find('h2') or
                element.find('h3') or
                element.find('a')
            )
            title = title_elem.get_text(strip=True) if title_elem else None

            if not title:
                return None

            # Find link
            link_elem = element.find('a', href=True)
            link = link_elem['href'] if link_elem else source_info['url']

            # Make relative URLs absolute
            if link and not link.startswith('http'):
                base_url = '/'.join(source_info['url'].split('/')[:3])
                link = base_url + (link if link.startswith('/') else '/' + link)

            # Find description
            desc_elem = (
                element.find('p') or
                element.find(class_=re.compile('description|excerpt|summary', re.I))
            )
            description = desc_elem.get_text(strip=True) if desc_elem else title

            # Try to find date
            published = self._extract_date(element)

            # Skip if too old
            if published and published < self.cutoff_time:
                return None

            article = {
                'title': title,
                'link': link,
                'description': description[:500],  # Limit description length
                'published': published or datetime.now(),
                'source': source_info['name']
            }

            return article

        except Exception as e:
            return None

    def _extract_date(self, element) -> Optional[datetime]:
        """Try to extract a date from an element"""
        # Look for common date patterns
        date_patterns = [
            'time',
            '[class*="date"]',
            '[class*="time"]',
            '[class*="published"]',
            'span.date',
            'span.time'
        ]

        for pattern in date_patterns:
            date_elem = element.select_one(pattern)
            if date_elem:
                # Try datetime attribute first
                if date_elem.get('datetime'):
                    try:
                        return date_parser.parse(date_elem['datetime']).replace(tzinfo=None)
                    except:
                        pass

                # Try parsing text content
                date_text = date_elem.get_text(strip=True)
                try:
                    return date_parser.parse(date_text, fuzzy=True).replace(tzinfo=None)
                except:
                    pass

        # Default to now if no date found
        return None

    def _is_relevant(self, article: Dict) -> bool:
        """Check if article is relevant based on keywords"""
        text = f"{article['title']} {article['description']}".lower()

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
        all_articles = self.scrape_all_sources()
        return all_articles[:max_articles]
