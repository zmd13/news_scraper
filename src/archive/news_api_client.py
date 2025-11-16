"""NewsAPI Client for fetching news articles"""
from newsapi import NewsApiClient
from datetime import datetime, timedelta
from typing import List, Dict
import os
from dotenv import load_dotenv


class NewsAPIFetcher:
    """Fetches news articles using NewsAPI"""

    def __init__(self, api_key: str, keywords: List[str], time_window_hours: int = 24, domains: str = None):
        """
        Initialize the NewsAPI fetcher

        Args:
            api_key: NewsAPI API key
            keywords: List of keywords to identify relevant articles
            time_window_hours: How far back to look for news (in hours)
            domains: Comma-separated string of domains to search (optional)
        """
        self.client = NewsApiClient(api_key=api_key)
        self.keywords = [kw.lower() for kw in keywords]
        self.time_window_hours = time_window_hours
        self.domains = domains

        # Calculate date range
        self.to_date = datetime.now()
        self.from_date = self.to_date - timedelta(hours=time_window_hours)

    def search_by_queries(self, queries: List[str], max_results_per_query: int = 50) -> List[Dict]:
        """
        Search for articles using multiple queries

        Args:
            queries: List of search query strings
            max_results_per_query: Maximum results per query

        Returns:
            List of article dictionaries
        """
        all_articles = []
        seen_urls = set()  # Avoid duplicates

        for query in queries:
            try:
                print(f"  Searching: \"{query}\"")
                articles = self._search_single_query(query, max_results_per_query)

                # Filter out duplicates
                unique_articles = []
                for article in articles:
                    if article['link'] not in seen_urls:
                        seen_urls.add(article['link'])
                        unique_articles.append(article)

                all_articles.extend(unique_articles)
                print(f"  ✓ Found {len(unique_articles)} unique articles (query: \"{query[:50]}...\")")

            except Exception as e:
                print(f"  ✗ Error searching \"{query}\": {str(e)}")

        # Sort by publication date (newest first)
        all_articles.sort(key=lambda x: x.get('published', datetime.min), reverse=True)

        return all_articles

    def _search_single_query(self, query: str, max_results: int) -> List[Dict]:
        """Search for articles using a single query"""
        articles = []

        try:
            # Build API parameters
            params = {
                'q': query,
                'from_param': self.from_date.strftime('%Y-%m-%d'),
                'to': self.to_date.strftime('%Y-%m-%d'),
                'language': 'en',
                'sort_by': 'publishedAt',
                'page_size': min(max_results, 100)  # NewsAPI max is 100
            }

            # Add domains if specified
            if self.domains:
                params['domains'] = self.domains

            # Call NewsAPI
            response = self.client.get_everything(**params)

            if response['status'] == 'ok':
                for article_data in response['articles']:
                    article = self._convert_to_standard_format(article_data)
                    if article and self._is_relevant(article):
                        articles.append(article)

        except Exception as e:
            raise Exception(f"NewsAPI error: {str(e)}")

        return articles

    def _convert_to_standard_format(self, article_data: Dict) -> Dict:
        """Convert NewsAPI format to our standard article format"""
        try:
            # Parse publication date
            published_str = article_data.get('publishedAt', '')
            if published_str:
                # Remove 'Z' and parse
                published = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
                published = published.replace(tzinfo=None)
            else:
                published = datetime.now()

            # Get description
            description = article_data.get('description') or article_data.get('content') or article_data.get('title', '')

            article = {
                'title': article_data.get('title', 'No Title'),
                'link': article_data.get('url', ''),
                'description': description[:500] if description else '',
                'published': published,
                'source': article_data.get('source', {}).get('name', 'Unknown')
            }

            return article

        except Exception as e:
            return None

    def _is_relevant(self, article: Dict) -> bool:
        """Check if article is relevant based on keywords"""
        text = f"{article['title']} {article['description']}".lower()

        # Check if any keyword appears in the text
        for keyword in self.keywords:
            if keyword in text:
                return True

        return False


def load_api_key() -> str:
    """Load NewsAPI key from environment"""
    # Load .env file from parent directory
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    load_dotenv(env_path)

    api_key = os.getenv('NEWSAPI_KEY')
    if not api_key:
        raise ValueError("NEWSAPI_KEY not found in .env file")

    return api_key
