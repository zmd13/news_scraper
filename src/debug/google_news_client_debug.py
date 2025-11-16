"""Google News Client - DEBUG VERSION with duplicate tracking"""
from gnews import GNews
from datetime import datetime, timedelta
from typing import List, Dict
import re


class GoogleNewsFetcherDebug:
    """Fetches news articles using Google News RSS - DEBUG VERSION"""

    def __init__(self, keywords: List[str], period: str = "7d", language: str = "en", country: str = "US"):
        """
        Initialize the Google News fetcher

        Args:
            keywords: List of keywords to identify relevant articles
            period: Time period (e.g., '7d', '24h', '1m')
            language: Language code (default: 'en')
            country: Country code (default: 'US')
        """
        self.keywords = [kw.lower() for kw in keywords]
        self.period = period

        # Initialize GNews client
        self.client = GNews(
            language=language,
            country=country,
            period=period,
            max_results=100  # Max per query
        )

    def _extract_keywords(self, title: str) -> set:
        """Extract important keywords from title for fuzzy matching"""
        # Remove source suffix if present
        if ' - ' in title:
            title = title.rsplit(' - ', 1)[0]

        # Convert to lowercase
        title = title.lower()

        # Remove common stopwords
        stopwords = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he',
            'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 'with',
            'their', 'this', 'but', 'they', 'have', 'had', 'what', 'when', 'where', 'who',
            'which', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
            'other', 'some', 'such', 'than', 'too', 'very', 'can', 'just', 'should', 'now'
        }

        # Remove common healthcare/industry terms that appear in many articles
        healthcare_common_terms = {
            'value', 'based', 'care', 'medicare', 'advantage', 'health', 'healthcare',
            'cms', 'medical', 'patient', 'patients', 'provider', 'providers',
            'plan', 'plans', 'program', 'model', 'new', 'report', 'reports',
            'announces', 'update', 'news', '2025', '2024', 'quarter', 'q3',
            'says', 'gets', 'launches', 'releases', 'year'
        }

        # Extract words (alphanumeric sequences)
        words = re.findall(r'\b[a-z0-9]+\b', title)

        # Filter out stopwords, healthcare common terms, and short words
        keywords = {word for word in words
                   if word not in stopwords
                   and word not in healthcare_common_terms
                   and len(word) > 2}

        return keywords

    def _is_similar_title(self, title1: str, title2: str, threshold: float = 0.40) -> Dict:
        """Check if two titles are similar - returns dict with similarity info"""
        keywords1 = self._extract_keywords(title1)
        keywords2 = self._extract_keywords(title2)

        # If either title has no keywords, not similar
        if not keywords1 or not keywords2:
            return {'is_duplicate': False, 'reason': None, 'similarity': 0}

        # Calculate Jaccard similarity (intersection / union)
        intersection = keywords1 & keywords2
        union = keywords1 | keywords2

        similarity = len(intersection) / len(union) if union else 0

        # Special case: If 2+ rare/specific company/product names match
        rare_words = {word for word in intersection if len(word) >= 7}

        if len(rare_words) >= 2:
            return {
                'is_duplicate': True,
                'reason': f'2+ company names match: {sorted(rare_words)}',
                'similarity': similarity,
                'keywords_overlap': sorted(intersection)
            }

        if len(intersection) >= 4 and similarity >= 0.30:
            return {
                'is_duplicate': True,
                'reason': f'4+ keywords with {similarity:.0%} similarity',
                'similarity': similarity,
                'keywords_overlap': sorted(intersection)
            }

        if similarity >= threshold:
            return {
                'is_duplicate': True,
                'reason': f'High similarity ({similarity:.0%})',
                'similarity': similarity,
                'keywords_overlap': sorted(intersection)
            }

        return {'is_duplicate': False, 'reason': None, 'similarity': similarity}

    def search_by_queries(self, queries: List[str], max_results_per_query: int = 50) -> List[Dict]:
        """
        Search for articles using multiple queries - DEBUG VERSION
        Marks duplicates but keeps them in the output
        """
        all_articles = []
        seen_urls = set()
        seen_titles = []

        for query in queries:
            try:
                print(f"  Searching: \"{query}\"")
                articles = self._search_single_query(query, max_results_per_query)

                # Check all articles, mark duplicates
                for article in articles:
                    # Check URL duplicate
                    if article['link'] in seen_urls:
                        article['is_duplicate'] = True
                        article['duplicate_reason'] = 'Duplicate URL'
                        all_articles.append(article)
                        continue

                    title = article['title']

                    # Check for exact title match
                    if ' - ' in title:
                        title_normalized = title.rsplit(' - ', 1)[0].lower().strip()
                    else:
                        title_normalized = title.lower().strip()

                    exact_match = any(title_normalized == seen.lower().strip() for seen in seen_titles)
                    if exact_match:
                        article['is_duplicate'] = True
                        article['duplicate_reason'] = 'Exact title match'
                        all_articles.append(article)
                        continue

                    # Check fuzzy match
                    fuzzy_result = None
                    for seen in seen_titles:
                        result = self._is_similar_title(title, seen)
                        if result['is_duplicate']:
                            fuzzy_result = result
                            break

                    if fuzzy_result:
                        article['is_duplicate'] = True
                        article['duplicate_reason'] = f"Fuzzy match: {fuzzy_result['reason']}"
                        article['duplicate_similarity'] = fuzzy_result['similarity']
                        article['duplicate_keywords'] = fuzzy_result.get('keywords_overlap', [])
                        all_articles.append(article)
                        continue

                    # Article is unique
                    article['is_duplicate'] = False
                    article['duplicate_reason'] = None
                    seen_urls.add(article['link'])
                    seen_titles.append(title)
                    all_articles.append(article)

                unique_count = sum(1 for a in articles if not a.get('is_duplicate', False))
                dup_count = len(articles) - unique_count
                print(f"  ✓ Found {unique_count} unique, {dup_count} duplicates (query: \"{query[:50]}...\")")

            except Exception as e:
                print(f"  ✗ Error searching \"{query}\": {str(e)}")

        # Sort by publication date (newest first)
        all_articles.sort(key=lambda x: x.get('published', datetime.min), reverse=True)

        return all_articles

    def _search_single_query(self, query: str, max_results: int) -> List[Dict]:
        """Search for articles using a single query"""
        articles = []

        try:
            # Update max results for this query
            self.client.max_results = min(max_results, 100)

            # Search Google News
            results = self.client.get_news(query)

            for result in results:
                article = self._convert_to_standard_format(result)
                if article and self._is_relevant(article):
                    articles.append(article)

        except Exception as e:
            raise Exception(f"Google News error: {str(e)}")

        return articles

    def _convert_to_standard_format(self, article_data: Dict) -> Dict:
        """Convert Google News format to our standard article format"""
        try:
            # Parse publication date
            published_str = article_data.get('published date', '')
            if published_str:
                try:
                    published = datetime.strptime(published_str, "%a, %d %b %Y %H:%M:%S %Z")
                except:
                    published = datetime.now()
            else:
                published = datetime.now()

            # Get description
            description = article_data.get('description', '') or article_data.get('title', '')

            article = {
                'title': article_data.get('title', 'No Title'),
                'link': article_data.get('url', ''),
                'description': description[:500] if description else '',
                'published': published,
                'source': article_data.get('publisher', {}).get('title', 'Unknown') if isinstance(article_data.get('publisher'), dict) else 'Unknown'
            }

            return article

        except Exception as e:
            return None

    def _is_relevant(self, article: Dict) -> bool:
        """Check if article is relevant - Two-stage filtering"""
        text = f"{article['title']} {article['description']}".lower()
        source = article.get('source', '').lower()

        # STAGE 1: BAD SOURCE BLOCKLIST
        blocked_sources = [
            'newser.com',
            '富途牛牛',
            'the kenya times',
            'tuko news',
            'fundação cultural do pará',
            'rs web solutions',
        ]

        for blocked in blocked_sources:
            if blocked in source:
                return False

        # Block legal spam patterns
        legal_spam_indicators = ['investigation alert', 'investor news', 'law firm', 'eagel & squire']
        if any(indicator in source for indicator in legal_spam_indicators):
            return False

        # STAGE 2: CONTENT-BASED FILTERING
        stock_spam_terms = [
            'bollinger bands', 'macd trends', 'swing trade', 'stock prediction',
            'price action summary', 'momentum entry alerts', 'breakout alerts',
            'volatility report', 'weekly high return', 'technical buy zone',
            'stop loss', 'high conviction investment', 'chart breakout',
            'trade entry summary', 'buy zone picks', 'momentum entry',
            'portfolio risk report', 'fast exit and entry'
        ]

        if any(spam in text for spam in stock_spam_terms):
            return False

        # Geographic irrelevance
        kenyan_education_terms = ['ksh', 'kenyan', 'kenya', 'ruto', 'ogamba']
        if any(term in text for term in kenyan_education_terms):
            return False

        # Topic irrelevance
        if 'cmmi' in text and any(term in text for term in ['cybersecurity', 'software development', 'maturity level']):
            healthcare_context = ['medicare', 'medicaid', 'health', 'cms', 'innovation']
            if not any(ctx in text for ctx in healthcare_context):
                return False

        if 'cms' in text:
            cms_software_terms = ['cms platform', 'content management', 'cms integration', 'frontend hosting']
            if any(term in text for term in cms_software_terms):
                return False
            healthcare_context = ['medicare', 'medicaid', 'health', 'hospital', 'physician', 'patient', 'medical']
            if not any(ctx in text for ctx in healthcare_context):
                return False

        sports_terms = ['basketball', 'football', 'soccer', 'nba', 'nfl', 'mlb', 'doubles crown', 'nationals 2025']
        if any(term in text for term in sports_terms):
            return False

        if 'ipa' in text:
            sports_indicators = ['nationals', 'doubles', 'tournament', 'championship', 'pickleball']
            if any(indicator in text for indicator in sports_indicators):
                return False

        if 'arcadia' in text:
            sports_indicators = ['basketball', 'team', 'pasadena', 'squad', 'athlete']
            if any(indicator in text for indicator in sports_indicators):
                return False

        irrelevant_terms = [
            'nuclear energy', 'clean energy', 'renewable energy',
            'e-commerce', 'python package', 'pypi',
            'gaming', 'video game', 'esports'
        ]

        if any(term in text for term in irrelevant_terms):
            return False

        # Legal spam
        legal_spam_terms = [
            'investigation alert', 'investor alert', 'securities claims',
            'suffered losses', 'encourages investors to contact',
            'law firm announces investigation', 'shareholder rights'
        ]

        if any(spam in text for spam in legal_spam_terms):
            return False

        # Must match at least one keyword
        for keyword in self.keywords:
            if keyword in text:
                return True

        return False
