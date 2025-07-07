import re
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from typing import List, Dict, Optional
import logging
import random
import time
from app.config.search_config import SearchConfig
from app.entities.search import SearchResult

logger = logging.getLogger(__name__)


class SearchService:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(SearchConfig.DEFAULT_HEADERS)
        self.session.headers["User-Agent"] = random.choice(SearchConfig.USER_AGENTS)

    def search_google(self, query: str, num_results: int = 10) -> List[str]:
        """
        Search Google and return top URLs
        """
        try:
            # Validate number of results
            num_results = SearchConfig.validate_num_results(num_results)

            urls = []
            for url in search(
                query,
                num_results=num_results,
                # stop=num_results,
                # pause=SearchConfig.SEARCH_DELAY,
            ):
                urls.append(url)
            return urls
        except Exception as e:
            logger.error(f"Error searching Google: {str(e)}")
            return []

    def fetch_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse HTML content from a URL
        """
        try:
            response = self.session.get(url, timeout=SearchConfig.TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Add small delay to be respectful
            time.sleep(0.5)
            return soup
        except Exception as e:
            logger.error(f"Error fetching content from {url}: {str(e)}")
            return None

    def extract_prices(self, soup: BeautifulSoup) -> List[str]:
        """
        Extract prices from HTML content using various patterns
        """
        prices = []

        # Use price patterns from config
        price_patterns = SearchConfig.get_price_patterns()

        # Search in text content
        text_content = soup.get_text()
        for pattern in price_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            prices.extend(matches)

        # Search in specific HTML elements commonly used for prices
        price_selectors = [
            '[class*="price"]',
            '[class*="cost"]',
            '[class*="amount"]',
            '[id*="price"]',
            "[data-price]",
            ".price",
            ".cost",
            ".amount",
            'span[class*="price"]',
            'div[class*="price"]',
            'p[class*="price"]',
        ]

        for selector in price_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                for pattern in price_patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    prices.extend(matches)

        # Remove duplicates while preserving order
        unique_prices = []
        seen = set()
        for price in prices:
            if price not in seen:
                unique_prices.append(price)
                seen.add(price)

        return unique_prices

    def extract_product_name(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract product name from HTML content
        """
        title_selectors = ["h1", "title", '[class*="title"]', '[class*="name"]']
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return None
    
    def extract_product_info(self, soup: BeautifulSoup) -> SearchResult:
        """
        Extract product information including title, description, and prices
        """
        info: SearchResult = SearchResult(
            link="",
            prices=[],
            product_name=None,
            currency=None,
        )

        # Extract title
        info.product_name = self.extract_product_name(soup)

        # Extract prices
        info.prices = self.extract_prices(soup)

        return info

    def search_and_extract(self, query: str, num_results: int) -> List[Dict]:
        """
        Search Google and extract product information from results
        """
        urls = self.search_google(query, num_results)
        results = []

        for i, url in enumerate(urls):
            logger.info(f"Processing URL {i + 1}/{len(urls)}: {url}")
            soup = self.fetch_page_content(url)

            if soup:
                info = self.extract_product_info(soup)
                info.link = url
                info.rank = i + 1
                results.append(info)
            else:
                logger.warning(f"Failed to fetch content from: {url}")

        return results

    def search(self, query: str, num_results: int | None) -> Dict:
        num_results = num_results or 2
        try:
            results = self.search_and_extract(query, num_results)
            return {"query": query, "total_results": len(results), "results": results}
        except Exception as e:
            logger.error(f"Error in search: {str(e)}")
            return {"query": query, "total_results": 0, "results": [], "error": str(e)}
