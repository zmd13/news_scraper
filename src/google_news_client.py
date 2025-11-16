"""Google News Client for fetching news articles"""
from gnews import GNews
from datetime import datetime, timedelta
from typing import List, Dict
import re


class GoogleNewsFetcher:
    """Fetches news articles using Google News RSS"""

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
        # These are too generic to indicate duplicate stories
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

    def _is_similar_title(self, title1: str, title2: str, threshold: float = 0.40) -> bool:
        """Check if two titles are similar using keyword overlap"""
        keywords1 = self._extract_keywords(title1)
        keywords2 = self._extract_keywords(title2)

        # If either title has no keywords, not similar
        if not keywords1 or not keywords2:
            return False

        # Calculate Jaccard similarity (intersection / union)
        intersection = keywords1 & keywords2
        union = keywords1 | keywords2

        similarity = len(intersection) / len(union) if union else 0

        # Special case: If 2+ rare/specific company/product names match
        # These are strong indicators of the same story even with different wording
        # Look for company names, product names, or unique identifiers (longer words)
        rare_words = {word for word in intersection if len(word) >= 7}  # 7+ chars = likely company/product name

        if len(rare_words) >= 2:
            # Two unique company/product names matching = very likely same story
            return True

        if len(intersection) >= 4 and similarity >= 0.30:
            # 4+ keywords with 30%+ similarity = likely same story
            return True

        return similarity >= threshold

    def categorize_article(self, article: Dict) -> str:
        """Categorize article based on title and description"""
        text = f"{article['title']} {article['description']}".lower()

        # Category 1: Industry Analysis (4 articles)
        if any(term in text for term in ['transformation imperative', 'what is value-based care', 'consulting', 'thought leadership', 'analysis:', 'deep dive', 'outlook', 'milliman analysis', 'pension']):
            return "Industry Analysis"

        # Category 2: Risk Adjustment & Actuarial (6 articles)
        if any(term in text for term in ['risk adjustment', 'radv', 'hcc', 'raf score', 'actuarial', 'fraud waste abuse', 'guardrails for ai in medicare']):
            return "Risk Adjustment & Actuarial"

        # Category 3: CMS Rules & Policy (18 articles)
        if any(term in text for term in ['cms finalizes', 'cms releases', 'cms will launch', 'physician fee schedule', 'cms calls back', 'cms lifts', 'cms extends', 'cmmi', 'medicaid drug', 'most favored nation', 'prior authorization', 'wiser model', 'interoperability', 'bona fide']):
            return "CMS Rules & Policy"

        # Category 4: Value-Based Care Models (15 articles)
        if any(term in text for term in ['value-based care succeeding', 'vbc', 'value-based care contracts', 'physician-level measurement', 'reinventing value-based', 'investing in tech for value', 'making value-based care', 'overlooked frontier', 'participation in value-based', 'momentum for value-based', 'what is value-based care']):
            return "Value-Based Care Models"

        # Category 5: Technology & Platforms (10 articles)
        if any(term in text for term in ['innovaccer', 'lightbeam', 'vim to accelerate', 'notifai', 'martlet.ai', 'nvidia', 'ai framework', 'analytics for vbc', 'gravity platform', 'ai agents', 'digital patient']):
            return "Technology & Platforms"

        # Category 6: Provider Contracts & Disputes (8 articles)
        if any(term in text for term in ['wakemed', 'negotiations', 'ballad health sues', 'fairview access at risk', 'home health providers notch', 'lawsuit', 'contract', 'dispute']):
            return "Provider Contracts & Disputes"

        # Category 7: Medicare Advantage Market (20 articles)
        if any(term in text for term in ['medicare advantage', 'ma plans', 'ma enrollees', 'insurers cutting', 'seniors must pick', 'discontinued medicare advantage', 'ma enrollment', 'myths about medicare advantage', 'turmoil in medicare advantage', 'ma market', 'directory errors']):
            return "Medicare Advantage Market"

        # Category 8: M&A and Partnerships (6 articles)
        if any(term in text for term in ['acquired', 'acquires', 'merger', 'vatica health', 'partnership', 'collaboration', 'humana and providence']):
            return "M&A and Partnerships"

        # Category 9: ACO Performance (12 articles)
        if any(term in text for term in ['aco saves', 'aco earns', 'aco distributes', 'shared savings', 'mssp results', 'aco performance', 'stellar health', 'pom aco', 'wellspan', 'ochsner']):
            return "ACO Performance"

        # Category 10: Company Earnings & Financial Performance (25 articles)
        if any(term in text for term in ['earnings call', 'q3 2025', 'quarterly', 'stock', 'shares', 'price target', 'analyst', 'nyse', 'rating', 'agilon health', 'financial results', 'revenue']):
            return "Company Earnings & Financial Performance"

        # Default fallback
        return "Other"

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
        seen_urls = set()  # Avoid duplicates by URL
        seen_titles = []  # List of seen titles for fuzzy matching

        for query in queries:
            try:
                print(f"  Searching: \"{query}\"")
                articles = self._search_single_query(query, max_results_per_query)

                # Filter out duplicates by URL, exact title, and fuzzy title match
                unique_articles = []
                for article in articles:
                    # Skip if URL already seen
                    if article['link'] in seen_urls:
                        continue

                    title = article['title']

                    # Check for exact title match (after normalizing)
                    if ' - ' in title:
                        title_normalized = title.rsplit(' - ', 1)[0].lower().strip()
                    else:
                        title_normalized = title.lower().strip()

                    # Check exact match
                    exact_match = any(title_normalized == seen.lower().strip() for seen in seen_titles)
                    if exact_match:
                        continue

                    # Check fuzzy match against all seen titles
                    fuzzy_match = any(self._is_similar_title(title, seen) for seen in seen_titles)
                    if fuzzy_match:
                        continue

                    # Article is unique - add it
                    seen_urls.add(article['link'])
                    seen_titles.append(title)
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
                # GNews returns format like "Mon, 11 Nov 2025 12:30:00 GMT"
                try:
                    published = datetime.strptime(published_str, "%a, %d %b %Y %H:%M:%S %Z")
                except:
                    # Fallback to current time if parsing fails
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
        """Check if article is relevant - Two-stage filtering: bad sources + irrelevant content"""
        text = f"{article['title']} {article['description']}".lower()
        source = article.get('source', '').lower()

        # STAGE 1: BAD SOURCE BLOCKLIST
        # Block consistently low-quality or spam sources
        blocked_sources = [
            'newser.com',                    # Stock technical analysis spam
            '富途牛牛',                        # Chinese financial site
            'the kenya times',               # Kenyan news (wrong geography)
            'tuko news',                     # Kenyan news
            'fundação cultural do pará',     # Brazilian cultural foundation
            'rs web solutions',              # CMMI cybersecurity (not healthcare)
        ]

        for blocked in blocked_sources:
            if blocked in source:
                return False

        # Block legal spam patterns in source names
        legal_spam_indicators = ['investigation alert', 'investor news', 'law firm', 'eagel & squire']
        if any(indicator in source for indicator in legal_spam_indicators):
            return False

        # STAGE 2: CONTENT-BASED IRRELEVANT FILTERING

        # 2.1 Stock Spam Keywords
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

        # 2.2 Geographic Irrelevance
        # Kenyan education context (wrong "capitation")
        kenyan_education_terms = ['ksh', 'kenyan', 'kenya', 'ruto', 'ogamba']
        if any(term in text for term in kenyan_education_terms):
            return False

        # 2.3 Topic Irrelevance

        # CMMI cybersecurity (not healthcare CMMI)
        if 'cmmi' in text and any(term in text for term in ['cybersecurity', 'software development', 'maturity level']):
            healthcare_context = ['medicare', 'medicaid', 'health', 'cms', 'innovation']
            if not any(ctx in text for ctx in healthcare_context):
                return False

        # CMS content management (not Centers for Medicare & Medicaid)
        if 'cms' in text:
            cms_software_terms = ['cms platform', 'content management', 'cms integration', 'frontend hosting']
            if any(term in text for term in cms_software_terms):
                return False
            # Require healthcare context for CMS
            healthcare_context = ['medicare', 'medicaid', 'health', 'hospital', 'physician', 'patient', 'medical']
            if not any(ctx in text for ctx in healthcare_context):
                return False

        # Sports (basketball, etc.)
        sports_terms = ['basketball', 'football', 'soccer', 'nba', 'nfl', 'mlb', 'doubles crown', 'nationals 2025']
        if any(term in text for term in sports_terms):
            return False

        # IPA sports context (not Independent Physician Association)
        if 'ipa' in text:
            sports_indicators = ['nationals', 'doubles', 'tournament', 'championship', 'pickleball']
            if any(indicator in text for indicator in sports_indicators):
                return False

        # Arcadia sports context (not Arcadia healthcare company)
        if 'arcadia' in text:
            sports_indicators = ['basketball', 'team', 'pasadena', 'squad', 'athlete']
            if any(indicator in text for indicator in sports_indicators):
                return False

        # Other irrelevant topics
        irrelevant_terms = [
            'nuclear energy', 'clean energy', 'renewable energy',
            'e-commerce', 'python package', 'pypi',
            'gaming', 'video game', 'esports'
        ]

        if any(term in text for term in irrelevant_terms):
            return False

        # 2.4 Legal Investigation Spam
        legal_spam_terms = [
            'investigation alert', 'investor alert', 'securities claims',
            'suffered losses', 'encourages investors to contact',
            'law firm announces investigation', 'shareholder rights'
        ]

        if any(spam in text for spam in legal_spam_terms):
            return False

        # FINAL CHECK: Article must match at least one keyword
        for keyword in self.keywords:
            if keyword in text:
                return True

        return False
