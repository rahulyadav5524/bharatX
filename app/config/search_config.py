import os
from typing import Dict, Any


class SearchConfig:
    """Configuration class for search service"""

    # Rate limiting
    SEARCH_DELAY = float(
        os.getenv("SEARCH_DELAY", "2.0")
    )  # Delay between searches in seconds
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

    # Search limits
    MAX_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "20"))
    DEFAULT_RESULTS = int(os.getenv("DEFAULT_SEARCH_RESULTS", "5"))

    # User agents for different requests
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    ]

    # Headers for requests
    DEFAULT_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    # Price patterns for different currencies
    PRICE_PATTERNS = {
        "USD": r"\$\d+(?:,\d{3})*(?:\.\d{2})?",
        "INR": r"₹\d+(?:,\d{3})*(?:\.\d{2})?",
        "EUR": r"€\d+(?:,\d{3})*(?:\.\d{2})?",
        "GBP": r"£\d+(?:,\d{3})*(?:\.\d{2})?",
        "JPY": r"¥\d+(?:,\d{3})*",
        "GENERIC": r"\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:USD|INR|EUR|GBP|JPY)",
    }

    # Site-specific configurations
    SITE_CONFIGS = {
        "amazon": {
            "delay": 3.0,
            "max_pages": 5,
            "selectors": {
                "title": "#productTitle",
                "price": ".a-price .a-offscreen",
                "rating": '[data-hook="average-star-rating"]',
            },
        },
        "flipkart": {
            "delay": 2.0,
            "max_pages": 3,
            "selectors": {
                "title": "h1, .B_NuCI",
                "price": "._30jeq3._16Jk6d",
                "rating": "._3LWZlK",
            },
        },
        "myntra": {
            "delay": 2.0,
            "max_pages": 3,
            "selectors": {
                "title": "h1.pdp-title",
                "price": ".pdp-price strong",
                "rating": ".index-overallRating",
            },
        },
    }

    @classmethod
    def get_site_config(cls, site_type: str) -> Dict[str, Any]:
        """Get configuration for a specific site"""
        return cls.SITE_CONFIGS.get(
            site_type, {"delay": cls.SEARCH_DELAY, "max_pages": 3, "selectors": {}}
        )

    @classmethod
    def get_price_patterns(cls) -> list:
        """Get all price patterns"""
        return list(cls.PRICE_PATTERNS.values())

    @classmethod
    def validate_num_results(cls, num_results: int) -> int:
        """Validate and limit the number of results"""
        if num_results <= 0:
            return cls.DEFAULT_RESULTS
        return min(num_results, cls.MAX_RESULTS)
