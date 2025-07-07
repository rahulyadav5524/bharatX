#!/usr/bin/env python3
"""
Comprehensive example demonstrating Google search with HTML parsing for price extraction
"""

import asyncio
import json
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.search import SearchService
from app.services.advanced_search import AdvancedSearchService


async def demonstrate_basic_search():
    """Demonstrate basic search functionality"""
    print("🔍 Basic Search Demonstration")
    print("=" * 50)

    search_service = SearchService()

    # Test with a product search
    query = "iPhone 15 Pro price India"
    print(f"Searching for: {query}")

    results = search_service.search(query, num_results=5)

    print(f"\nQuery: {results['query']}")
    print(f"Total results found: {results['total_results']}")

    for i, result in enumerate(results["results"], 1):
        print(f"\n--- Result {i} ---")
        print(f"🌐 URL: {result['url']}")
        print(f"📝 Title: {result['title'][:100]}...")
        print(f"📄 Description: {result['description'][:100]}...")
        print(f"💰 Prices found: {result['prices']}")
        if result["images"]:
            print(f"🖼️  Images: {len(result['images'])} found")
        print("-" * 40)


async def demonstrate_advanced_search():
    """Demonstrate advanced search with site-specific parsing"""
    print("\n🚀 Advanced Search Demonstration")
    print("=" * 50)

    advanced_service = AdvancedSearchService()

    # Test with specific e-commerce search
    query = "Samsung Galaxy S24 price"
    print(f"Searching for: {query}")

    results = advanced_service.enhanced_search(query, num_results=3)

    print(f"\nQuery: {results['query']}")
    print(f"Total results found: {results['total_results']}")

    for i, result in enumerate(results["results"], 1):
        print(f"\n--- Advanced Result {i} ---")
        print(f"🌐 URL: {result['url']}")
        print(f"🏪 Site Type: {result.get('site_type', 'unknown')}")
        print(f"📝 Title: {result.get('title', 'N/A')[:100]}...")

        # Show specific fields based on site type
        if result.get("site_type") in ["amazon", "flipkart", "myntra"]:
            print(f"💰 Price: {result.get('price', 'N/A')}")
            print(f"💸 Original Price: {result.get('original_price', 'N/A')}")
            print(f"🏷️  Discount: {result.get('discount', 'N/A')}")
            print(f"⭐ Rating: {result.get('rating', 'N/A')}")
            print(f"📊 Reviews: {result.get('reviews_count', 'N/A')}")
        else:
            print(f"💰 Prices found: {result.get('prices', [])}")

        if result.get("images"):
            print(f"🖼️  Images: {len(result['images'])} found")
        print("-" * 40)


def demonstrate_api_usage():
    """Demonstrate how to use the API"""
    print("\n📡 API Usage Example")
    print("=" * 50)

    # Example API request body
    api_request = {
        "query": "MacBook Pro M3 price",
        "country": "India",
        "num_results": 5,
    }

    print("Example API Request:")
    print(json.dumps(api_request, indent=2))

    print("\nTo test the API, start the FastAPI server:")
    print("python main.py")
    print("\nThen make a POST request to:")
    print("http://localhost:1000/search")
    print("\nWith the above JSON body.")


def price_comparison_example():
    """Example of price comparison across multiple sites"""
    print("\n💰 Price Comparison Example")
    print("=" * 50)

    search_service = SearchService()

    # Search for a specific product
    query = "iPhone 14 128GB price comparison"
    results = search_service.search(query, num_results=5)

    # Extract and display prices
    all_prices = []
    for result in results["results"]:
        if result["prices"]:
            for price in result["prices"]:
                all_prices.append(
                    {
                        "price": price,
                        "url": result["url"],
                        "title": result["title"][:50] + "...",
                    }
                )

    print(f"Found {len(all_prices)} prices:")
    for price_info in all_prices:
        print(f"💰 {price_info['price']} - {price_info['title']}")
        print(f"   🌐 {price_info['url']}")


def create_search_tips():
    """Display search tips for better results"""
    print("\n💡 Search Tips for Better Results")
    print("=" * 50)

    tips = [
        "🎯 Be specific: 'iPhone 14 Pro 256GB price' vs 'iPhone price'",
        "🌍 Include location: 'MacBook Pro price India' for local results",
        "🏪 Include store names: 'Samsung TV price Amazon Flipkart'",
        "📱 Include model numbers: 'Galaxy S24 Ultra 512GB' for exact matches",
        "🔄 Try variations: 'cost', 'rate', 'buy' instead of just 'price'",
        "📊 Use comparison terms: 'price comparison', 'best deals'",
        "🎉 Look for sales: 'iPhone discount offer sale'",
        "📅 Include time: 'iPhone 15 price 2024' for recent results",
    ]

    for tip in tips:
        print(tip)


async def main():
    """Main demonstration function"""
    print("🛍️  Google Search & Price Extraction Demo")
    print("=" * 60)

    try:
        # Basic search demo
        await demonstrate_basic_search()

        # Advanced search demo
        await demonstrate_advanced_search()

        # API usage example
        demonstrate_api_usage()

        # Price comparison example
        price_comparison_example()

        # Search tips
        create_search_tips()

    except Exception as e:
        print(f"❌ Error during demonstration: {str(e)}")
        print("Make sure you have installed all required packages:")
        print("pip install beautifulsoup4 requests googlesearch-python lxml html5lib")


if __name__ == "__main__":
    asyncio.run(main())
