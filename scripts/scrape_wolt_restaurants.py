#!/usr/bin/env python3
"""
Wolt Restaurants Scraper
Scrapes all Wolt restaurants and their menus from available cities and saves to CSV
"""

import json
import csv
import time
import requests
from pathlib import Path
from typing import List, Dict, Any
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API Configuration
BASE_URL = "https://consumer-api.wolt.com"
RESTAURANTS_API = f"{BASE_URL}/v1/pages/restaurants"
ITEMS_API = f"{BASE_URL}/consumer-api/consumer-assortment/v1/venues/slug"

# Headers from examples (modified to avoid brotli decoding issues)
HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate',  # Removed 'br, zstd' to fix Baku decoding error
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'app-language': 'az',
    'client-version': '1.16.75-PR20787',
    'clientversionnumber': '1.16.75-PR20787',
    'origin': 'https://wolt.com',
    'platform': 'Web',
    'referer': 'https://wolt.com/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'w-wolt-session-id': 'no-analytics-consent'
}

# Rate limiting
DELAY_BETWEEN_REQUESTS = 1  # seconds


def safe_join(items, separator=', '):
    """Safely join a list of items, converting non-strings to strings"""
    if not items:
        return ''
    try:
        return separator.join(str(item) if not isinstance(item, dict) else json.dumps(item) for item in items)
    except Exception:
        return str(items)


class WoltScraper:
    def __init__(self, cities_file: str = "examples/cities.json", max_cities: int = None, country_filter: str = None):
        self.cities_file = cities_file
        self.max_cities = max_cities
        self.country_filter = country_filter
        self.cities = []
        self.restaurants = []
        self.menu_items = []

    def load_cities(self) -> List[Dict]:
        """Load cities from JSON file"""
        logger.info(f"Loading cities from {self.cities_file}")
        with open(self.cities_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            cities = data.get('results', data if isinstance(data, list) else [])
            logger.info(f"Loaded {len(cities)} cities")
            return cities

    def fetch_restaurants_for_city(self, city: Dict) -> List[Dict]:
        """Fetch all restaurants for a given city"""
        city_name = city.get('name', city.get('slug', 'unknown'))
        coordinates = city.get('location', {}).get('coordinates', [])

        if len(coordinates) < 2:
            logger.warning(f"Invalid coordinates for city {city_name}")
            return []

        lon, lat = coordinates[0], coordinates[1]

        logger.info(f"Fetching restaurants for {city_name} (lat={lat}, lon={lon})")

        try:
            params = {'lat': lat, 'lon': lon}
            response = requests.get(RESTAURANTS_API, params=params, headers=HEADERS, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Extract venues from sections
            venues = []
            for section in data.get('sections', []):
                for item in section.get('items', []):
                    if item.get('template') == 'venue-large' and 'venue' in item:
                        venue = item['venue'].copy()
                        venue['city'] = city_name
                        venue['city_slug'] = city.get('slug', '')
                        venue['city_country'] = city.get('country_code_alpha3', city.get('country_code_alpha2', ''))
                        venues.append(venue)

            logger.info(f"Found {len(venues)} restaurants in {city_name}")
            time.sleep(DELAY_BETWEEN_REQUESTS)
            return venues

        except Exception as e:
            logger.error(f"Error fetching restaurants for {city_name}: {e}")
            return []

    def fetch_menu_items_for_restaurant(self, restaurant: Dict) -> List[Dict]:
        """Fetch all menu items for a given restaurant"""
        slug = restaurant.get('slug')
        restaurant_name = restaurant.get('name', slug)

        if not slug:
            logger.warning(f"No slug for restaurant {restaurant_name}")
            return []

        logger.info(f"Fetching menu for {restaurant_name} ({slug})")

        try:
            # First, get the basic venue info to retrieve item IDs
            url = f"{ITEMS_API}/{slug}/assortment"
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Extract all item IDs from categories
            item_ids = []
            for category in data.get('categories', []):
                item_ids.extend(category.get('item_ids', []))

            if not item_ids:
                logger.info(f"No items found for {restaurant_name}")
                return []

            # Fetch detailed item information
            items_url = f"{ITEMS_API}/{slug}/assortment/items"
            payload = {"item_ids": item_ids}
            headers_with_content = HEADERS.copy()
            headers_with_content['content-type'] = 'application/json'

            response = requests.post(items_url, json=payload, headers=headers_with_content, timeout=30)
            response.raise_for_status()
            items_data = response.json()

            # Process items
            items = []
            for item in items_data.get('items', []):
                item_info = {
                    'restaurant_id': restaurant.get('id'),
                    'restaurant_name': restaurant_name,
                    'restaurant_slug': slug,
                    'city': restaurant.get('city'),
                    'item_id': item.get('id'),
                    'item_name': item.get('name'),
                    'item_description': item.get('description', ''),
                    'item_price': item.get('price'),
                    'item_currency': restaurant.get('currency', 'AZN'),
                    'item_tags': safe_join(item.get('tags', [])),
                    'item_has_options': bool(item.get('options')),
                    'item_vat_percentage': item.get('vat_percentage'),
                }
                items.append(item_info)

            logger.info(f"Found {len(items)} menu items for {restaurant_name}")
            time.sleep(DELAY_BETWEEN_REQUESTS)
            return items

        except Exception as e:
            logger.error(f"Error fetching menu for {restaurant_name}: {e}")
            return []

    def flatten_restaurant_data(self, restaurant: Dict) -> Dict:
        """Flatten nested restaurant data for CSV export"""
        rating_data = restaurant.get('rating', {})
        location = restaurant.get('location', [])

        return {
            'id': restaurant.get('id'),
            'name': restaurant.get('name'),
            'slug': restaurant.get('slug'),
            'city': restaurant.get('city'),
            'city_slug': restaurant.get('city_slug'),
            'country': restaurant.get('city_country'),
            'address': restaurant.get('address', ''),
            'online': restaurant.get('online'),
            'delivers': restaurant.get('delivers'),
            'franchise': restaurant.get('franchise', ''),
            'product_line': restaurant.get('product_line', ''),
            'short_description': restaurant.get('short_description', ''),
            'tags': safe_join(restaurant.get('tags', [])),
            'currency': restaurant.get('currency'),
            'price_range': restaurant.get('price_range'),
            'delivery_price': restaurant.get('delivery_price', ''),
            'delivery_price_int': restaurant.get('delivery_price_int'),
            'estimate_min': restaurant.get('estimate_range', '').split('-')[0] if restaurant.get('estimate_range') else '',
            'estimate_max': restaurant.get('estimate_range', '').split('-')[-1] if restaurant.get('estimate_range') else '',
            'rating_score': rating_data.get('score'),
            'rating_count': rating_data.get('volume'),
            'location_lat': location[1] if len(location) > 1 else None,
            'location_lon': location[0] if len(location) > 0 else None,
        }

    def scrape_all(self):
        """Main scraping function"""
        logger.info("Starting Wolt scraper...")

        # Load cities
        all_cities = self.load_cities()

        # Filter by country if specified
        if self.country_filter:
            filtered_cities = [
                city for city in all_cities
                if city.get('country_code_alpha2', '').upper() == self.country_filter.upper() or
                   city.get('country_code_alpha3', '').upper() == self.country_filter.upper()
            ]
            logger.info(f"Filtered {len(filtered_cities)} cities from {self.country_filter} out of {len(all_cities)} total cities")
            all_cities = filtered_cities

        # Limit cities if max_cities is set
        if self.max_cities:
            self.cities = all_cities[:self.max_cities]
            logger.info(f"Limited to first {self.max_cities} cities out of {len(all_cities)} total")
        else:
            self.cities = all_cities

        # Scrape restaurants for each city
        all_restaurants = []
        all_menu_items = []

        for i, city in enumerate(self.cities, 1):
            logger.info(f"Processing city {i}/{len(self.cities)}: {city.get('name')}")

            # Fetch restaurants
            restaurants = self.fetch_restaurants_for_city(city)
            all_restaurants.extend(restaurants)

            # Fetch menu items for each restaurant
            for j, restaurant in enumerate(restaurants, 1):
                logger.info(f"  Processing restaurant {j}/{len(restaurants)}")
                menu_items = self.fetch_menu_items_for_restaurant(restaurant)
                all_menu_items.extend(menu_items)

        self.restaurants = all_restaurants
        self.menu_items = all_menu_items

        logger.info(f"Scraping complete! Found {len(self.restaurants)} restaurants and {len(self.menu_items)} menu items")

    def save_to_csv(self, output_dir: str = "data"):
        """Save scraped data to CSV files"""
        Path(output_dir).mkdir(exist_ok=True)

        # Save restaurants
        restaurants_file = f"{output_dir}/restaurants.csv"
        if self.restaurants:
            logger.info(f"Saving {len(self.restaurants)} restaurants to {restaurants_file}")
            flattened_restaurants = [self.flatten_restaurant_data(r) for r in self.restaurants]

            with open(restaurants_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=flattened_restaurants[0].keys())
                writer.writeheader()
                writer.writerows(flattened_restaurants)

        # Save menu items
        menu_file = f"{output_dir}/menu_items.csv"
        if self.menu_items:
            logger.info(f"Saving {len(self.menu_items)} menu items to {menu_file}")

            with open(menu_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.menu_items[0].keys())
                writer.writeheader()
                writer.writerows(self.menu_items)

        # Save combined data (restaurants with their menu items in a denormalized format)
        combined_file = f"{output_dir}/restaurants_with_menu.csv"
        logger.info(f"Saving combined data to {combined_file}")

        combined_data = []
        for restaurant in self.restaurants:
            restaurant_flat = self.flatten_restaurant_data(restaurant)

            # Find menu items for this restaurant
            restaurant_menu_items = [
                item for item in self.menu_items
                if item.get('restaurant_id') == restaurant.get('id')
            ]

            if restaurant_menu_items:
                for menu_item in restaurant_menu_items:
                    combined_row = {**restaurant_flat, **menu_item}
                    combined_data.append(combined_row)
            else:
                # Restaurant with no menu items
                combined_data.append(restaurant_flat)

        if combined_data:
            with open(combined_file, 'w', newline='', encoding='utf-8') as f:
                # Get all unique keys from combined data
                all_keys = set()
                for row in combined_data:
                    all_keys.update(row.keys())

                writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
                writer.writeheader()
                writer.writerows(combined_data)

        logger.info("All data saved successfully!")


def main():
    """Main entry point"""
    import sys

    # Parse command-line arguments
    max_cities = None
    country_filter = "AZ"  # Default to Azerbaijan

    if len(sys.argv) > 1:
        try:
            max_cities = int(sys.argv[1])
            logger.info(f"Limiting scrape to {max_cities} cities")
        except ValueError:
            logger.warning(f"Invalid max_cities argument: {sys.argv[1]}. Scraping all cities.")

    if len(sys.argv) > 2:
        country_filter = sys.argv[2]
        logger.info(f"Filtering by country: {country_filter}")

    scraper = WoltScraper(max_cities=max_cities, country_filter=country_filter)

    try:
        scraper.scrape_all()
        scraper.save_to_csv()

        logger.info("=" * 60)
        logger.info("SCRAPING COMPLETED SUCCESSFULLY!")
        logger.info(f"Total restaurants: {len(scraper.restaurants)}")
        logger.info(f"Total menu items: {len(scraper.menu_items)}")
        logger.info("=" * 60)

    except KeyboardInterrupt:
        logger.info("\n\nScraping interrupted by user. Saving partial data...")
        scraper.save_to_csv()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        logger.info("Attempting to save partial data...")
        scraper.save_to_csv()


if __name__ == "__main__":
    main()
