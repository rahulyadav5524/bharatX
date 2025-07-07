import re
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from typing import List, Dict, Optional, Tuple
import logging
import random
import time
from app.config.search_config import SearchConfig
from app.entities.search import SearchResult

logger = logging.getLogger(__name__)


class BaseService:
    _version = 1
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(SearchConfig.DEFAULT_HEADERS)
        self.session.headers["User-Agent"] = random.choice(SearchConfig.USER_AGENTS)

    def search_google(self, query: str, num_results: int = 10) -> List[str]:
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
        prices = []

        price_patterns = SearchConfig.get_price_patterns()

        text_content = soup.get_text()
        for pattern in price_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            prices.extend(matches)

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

        unique_prices = []
        seen = set()
        for price in prices:
            if price not in seen:
                unique_prices.append(price)
                seen.add(price)

        return unique_prices

    def extract_currency(self, price_text: str) -> Optional[str]:
        currency_patterns = {
            'INR': r'[₹]|rs\.?|rupees?|inr',
            'USD': r'[\$]|usd|dollars?',
            'EUR': r'[€]|eur|euros?',
            'GBP': r'[£]|gbp|pounds?',
            'JPY': r'[¥]|jpy|yen',
            'CNY': r'[¥]|cny|yuan',
            'KRW': r'[₩]|krw|won',
            'RUB': r'[₽]|rub|rubles?',
        }

        for currency, pattern in currency_patterns.items():
            if re.search(pattern, price_text, re.IGNORECASE):
                return currency
        
        return None
    
    def extract_product_name(self, soup: BeautifulSoup) -> Optional[str]:
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

        # Extract currency from the first price if available
        if info.prices:
            first_price = info.prices[0]
            info.currency = self.extract_currency(first_price)

        return info

    def search_and_extract(self, query: str, num_results: int) -> List[Dict]:
        urls = self.search_google(query, num_results)
        results = []

        for i, url in enumerate(urls):
            logger.info(f"Processing URL {i + 1}/{len(urls)}: {url}")
            soup = self.fetch_page_content(url)

            if soup:
                info = self.extract_product_info(soup)
                info.link = url
                # info.rank = i + 1
                if len(info.prices) == 0:
                    logger.warning(f"No prices found for URL: {url}")
                    continue

                results.append(info)
            else:
                logger.warning(f"Failed to fetch content from: {url}")

        return results

    def search(self, query: str, num_results: int | None = None) -> Dict:
        num_results = num_results or SearchConfig.DEFAULT_RESULTS
        try:
            results = self.search_and_extract(query, num_results)
            return {"query": query,  "results": results}
        except Exception as e:
            logger.error(f"Error in search: {str(e)}")
            return {"query": query, "results": [], "error": str(e)}

class SearchService(BaseService):
    _version = 2
    def normalize_price(self, price_text: str) -> Optional[Tuple[float, str]]:
        if not price_text:
            return None
        
        # Clean the price text
        cleaned_price = re.sub(r'[^\d.,₹$€£¥₩₽¢₨₪₫₦₡₵₴₸₲₱₾₺₼₿\s-]', '', price_text)
        
        # Currency patterns with their symbols
        currency_patterns = {
            'INR': r'[₹]|rs\.?|rupees?|inr',
            'USD': r'[\$]|usd|dollars?',
            'EUR': r'[€]|eur|euros?',
            'GBP': r'[£]|gbp|pounds?',
            'JPY': r'[¥]|jpy|yen',
            'CNY': r'[¥]|cny|yuan',
            'KRW': r'[₩]|krw|won',
            'RUB': r'[₽]|rub|rubles?',
        }
        
        # Find currency
        currency = None
        for curr_code, pattern in currency_patterns.items():
            if re.search(pattern, cleaned_price.lower()):
                currency = curr_code
                break
        
        # Extract numeric value
        numeric_match = re.search(r'(\d{1,3}(?:[,\s]\d{3})*(?:\.\d{2})?|\d+(?:\.\d{2})?)', cleaned_price)
        if numeric_match:
            numeric_str = numeric_match.group(1)
            # Remove thousand separators
            numeric_str = re.sub(r'[,\s]', '', numeric_str)
            try:
                value = float(numeric_str)
                return (value, currency or 'UNKNOWN')
            except ValueError:
                pass
        
        return None

    def extract_prices(self, soup: BeautifulSoup) -> List[Dict]:
        prices = []
        
        price_patterns = [
            # Indian Rupees
            r'₹\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'Rs\.?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'INR\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*₹',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*Rs\.?',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*INR',
            
            # US Dollars
            r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'USD\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*USD',
            
            # Euros
            r'€\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'EUR\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*€',
            
            # British Pounds
            r'£\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'GBP\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            
            # Generic price patterns
            r'Price:\s*([₹$€£¥₩₽¢₨₪₫₦₡₵₴₸₲₱₾₺₼₿]?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'Cost:\s*([₹$€£¥₩₽¢₨₪₫₦₡₵₴₸₲₱₾₺₼₿]?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'Amount:\s*([₹$€£¥₩₽¢₨₪₫₦₡₵₴₸₲₱₾₺₼₿]?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        ]
        
        price_selectors = [
            # Common price classes
            '.price', '.cost', '.amount', '.value',
            '[class*="price"]', '[class*="cost"]', '[class*="amount"]', '[class*="value"]',
            '[id*="price"]', '[id*="cost"]', '[id*="amount"]',
            
            # E-commerce specific
            '.sale-price', '.regular-price', '.current-price', '.final-price',
            '.product-price', '.item-price', '.listing-price',
            '[class*="sale-price"]', '[class*="regular-price"]', '[class*="current-price"]',
            
            # Schema.org microdata
            '[itemtype*="Product"] [itemprop="price"]',
            '[itemtype*="Offer"] [itemprop="price"]',
            '[itemtype*="PriceSpecification"] [itemprop="price"]',
            
            # Data attributes
            '[data-price]', '[data-cost]', '[data-amount]', '[data-value]',
            '[data-original-price]', '[data-sale-price]', '[data-current-price]',
            
            # Specific tags
            'span[class*="price"]', 'div[class*="price"]', 'p[class*="price"]',
            'span[class*="cost"]', 'div[class*="cost"]', 'p[class*="cost"]',
            'meta[property="product:price:amount"]',
            'meta[name="price"]',
            
            # JSON-LD structured data
            'script[type="application/ld+json"]'
        ]
        
        text_content = soup.get_text()
        for pattern in price_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            for match in matches:
                normalized = self.normalize_price(match)
                if normalized:
                    prices.append({
                        'raw_text': match,
                        'value': normalized[0],
                        'currency': normalized[1],
                        'source': 'text_content'
                    })
        
        for selector in price_selectors:
            try:
                elements = soup.select(selector)
                for element in elements:
                    if element.name == 'script' and element.get('type') == 'application/ld+json':
                        try:
                            import json
                            data = json.loads(element.string)
                            price_data = self.extract_price_from_json_ld(data)
                            if price_data:
                                prices.extend(price_data)
                            continue
                        except:
                            pass
                    
                    # Check data attributes first
                    for attr in ['data-price', 'data-cost', 'data-amount', 'data-value']:
                        if element.get(attr):
                            normalized = self.normalize_price(element.get(attr))
                            if normalized:
                                prices.append({
                                    'raw_text': element.get(attr),
                                    'value': normalized[0],
                                    'currency': normalized[1],
                                    'source': f'attribute_{attr}'
                                })
                    
                    # Check element text
                    text = element.get_text(strip=True)
                    if text:
                        for pattern in price_patterns:
                            matches = re.findall(pattern, text, re.IGNORECASE)
                            for match in matches:
                                normalized = self.normalize_price(match)
                                if normalized:
                                    prices.append({
                                        'raw_text': match,
                                        'value': normalized[0],
                                        'currency': normalized[1],
                                        'source': f'element_{selector}'
                                    })
            except Exception as e:
                logger.debug(f"Error processing selector {selector}: {str(e)}")
        
        unique_prices = []
        seen_values = set()
        
        for price in prices:
            price_key = (price['value'], price['currency'])
            if price_key not in seen_values:
                unique_prices.append(price)
                seen_values.add(price_key)
        
        unique_prices.sort(key=lambda x: x['value'])
        
        return unique_prices

    def extract_price_from_json_ld(self, data: Dict) -> List[Dict]:
        """
        Extract price information from JSON-LD structured data
        """
        prices = []
        
        def extract_from_dict(obj):
            if isinstance(obj, dict):
                # Check for price in offers
                if 'offers' in obj:
                    offers = obj['offers']
                    if isinstance(offers, list):
                        for offer in offers:
                            extract_from_dict(offer)
                    else:
                        extract_from_dict(offers)
                
                # Check for direct price
                if 'price' in obj:
                    price_value = obj['price']
                    currency = obj.get('priceCurrency', 'UNKNOWN')
                    
                    try:
                        if isinstance(price_value, str):
                            # Try to extract numeric value
                            numeric_match = re.search(r'(\d+(?:\.\d{2})?)', price_value)
                            if numeric_match:
                                price_value = float(numeric_match.group(1))
                        
                        if isinstance(price_value, (int, float)):
                            prices.append({
                                'raw_text': str(obj['price']),
                                'value': float(price_value),
                                'currency': currency,
                                'source': 'json_ld'
                            })
                    except:
                        pass
                
                # Recursively check nested objects
                for value in obj.values():
                    if isinstance(value, (dict, list)):
                        extract_from_dict(value)
            
            elif isinstance(obj, list):
                for item in obj:
                    extract_from_dict(item)
        
        extract_from_dict(data)
        return prices

    def get_best_price(self, prices: List[Dict]) -> Optional[Dict]:
        if not prices:
            return None
        
        realistic_prices = [
            p for p in prices 
            if 1 <= p['value'] <= 10000000  # Adjust range as needed
        ]
        
        if not realistic_prices:
            return None
        
        structured_prices = [
            p for p in realistic_prices 
            if p['source'] in ['json_ld', 'attribute_data-price', 'attribute_data-cost']
        ]
        
        if structured_prices:
            return structured_prices[0]  # Already sorted by value
        
        return realistic_prices[0]

    def extract_product_info(self, soup: BeautifulSoup) -> SearchResult:
        info: SearchResult = SearchResult(
            link="",
            prices=[],
            product_name=None,
            currency=None,
        )

        # Extract title
        info.product_name = self.extract_product_name(soup)

        # Extract prices with enhanced method
        extracted_prices = self.extract_prices(soup)
        info.prices = extracted_prices
        
        # Set currency from the best price
        best_price = self.get_best_price(extracted_prices)
        if best_price:
            info.currency = best_price['currency']

        return info
    

class SearchVersion:
    _latest_version = 1

    def __init__(self, version: int = None):
        self.version = max(1, min(version or self._latest_version, self._latest_version))

    def get_service(self) -> BaseService:
        if self.version == 1:
            return BaseService()
        elif self.version == 2:
            return SearchService()
        else:
            raise ValueError(f"Unsupported search service version: {self.version}")