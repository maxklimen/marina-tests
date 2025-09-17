"""
Sitemap XML handling for fetching and parsing sitemap data.
"""
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Set
from urllib.parse import urlparse
from config import Config


class SitemapHandler:
    """Handler for sitemap XML operations."""

    def __init__(self, environment: str = None):
        """Initialize sitemap handler with environment."""
        self.environment = environment or Config.CURRENT_ENV
        self.sitemap_url = Config.get_sitemap_url(self.environment)
        self.urls = []
        self.raw_xml = None

    def fetch_sitemap(self) -> bool:
        """Fetch sitemap XML from the website."""
        try:
            print(f"🔄 Fetching sitemap from: {self.sitemap_url}")

            response = requests.get(
                self.sitemap_url,
                timeout=Config.REQUEST_TIMEOUT,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )

            if response.status_code == 200:
                self.raw_xml = response.text
                print(f"✅ Sitemap fetched successfully ({len(self.raw_xml)} bytes)")
                return True
            else:
                print(f"❌ Failed to fetch sitemap: HTTP {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching sitemap: {e}")
            return False

    def parse_sitemap(self) -> List[str]:
        """Parse sitemap XML and extract URLs."""
        if not self.raw_xml:
            if not self.fetch_sitemap():
                return []

        try:
            # Parse XML
            root = ET.fromstring(self.raw_xml)

            # Handle XML namespaces
            namespaces = {
                'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'
            }

            # Extract URLs from sitemap
            urls = []
            for url_element in root.findall('.//sitemap:url', namespaces):
                loc_element = url_element.find('sitemap:loc', namespaces)
                if loc_element is not None and loc_element.text:
                    urls.append(loc_element.text.strip())

            # If no URLs found with namespace, try without namespace
            if not urls:
                for url_element in root.findall('.//url'):
                    loc_element = url_element.find('loc')
                    if loc_element is not None and loc_element.text:
                        urls.append(loc_element.text.strip())

            self.urls = urls
            print(f"✅ Parsed {len(urls)} URLs from sitemap")
            return urls

        except ET.ParseError as e:
            print(f"❌ Error parsing sitemap XML: {e}")
            return []

        except Exception as e:
            print(f"❌ Unexpected error parsing sitemap: {e}")
            return []

    def get_sitemap_urls(self) -> List[str]:
        """Get all URLs from sitemap."""
        if not self.urls:
            self.parse_sitemap()
        return self.urls

    def normalize_url_for_comparison(self, url: str) -> str:
        """Normalize URL for comparison purposes."""
        if not url:
            return ""

        # Remove protocol and trailing slash
        normalized = url.replace('https://', '').replace('http://', '')
        if normalized.endswith('/'):
            normalized = normalized[:-1]

        return normalized

    def check_url_in_sitemap(self, test_url: str) -> Dict:
        """Check if a URL exists in the sitemap."""
        sitemap_urls = self.get_sitemap_urls()
        normalized_test_url = self.normalize_url_for_comparison(test_url)

        # Normalize all sitemap URLs for comparison
        normalized_sitemap_urls = [
            self.normalize_url_for_comparison(url) for url in sitemap_urls
        ]

        is_present = normalized_test_url in normalized_sitemap_urls

        return {
            'url': test_url,
            'in_sitemap': is_present,
            'normalized_url': normalized_test_url
        }

    def validate_expected_urls(self, expected_urls: List[str]) -> Dict:
        """Validate that expected URLs are present in sitemap."""
        results = {
            'total_expected': len(expected_urls),
            'found_in_sitemap': 0,
            'missing_from_sitemap': [],
            'details': []
        }

        for url in expected_urls:
            check_result = self.check_url_in_sitemap(url)
            results['details'].append(check_result)

            if check_result['in_sitemap']:
                results['found_in_sitemap'] += 1
            else:
                results['missing_from_sitemap'].append(url)

        return results

    def validate_removed_urls(self, removed_urls: List[str]) -> Dict:
        """Validate that removed URLs are NOT present in sitemap."""
        results = {
            'total_removed': len(removed_urls),
            'still_in_sitemap': 0,
            'properly_removed': [],
            'still_present': [],
            'details': []
        }

        for url in removed_urls:
            check_result = self.check_url_in_sitemap(url)
            results['details'].append(check_result)

            if not check_result['in_sitemap']:
                results['properly_removed'].append(url)
            else:
                results['still_in_sitemap'] += 1
                results['still_present'].append(url)

        return results

    def get_sitemap_analysis(self, redirect_data: List[Dict], remove_data: List[Dict]) -> Dict:
        """Perform comprehensive sitemap analysis."""
        # Extract URLs for analysis
        expected_urls = [item['expected_url'] for item in redirect_data if item['expected_url'] != 'REMOVE']
        original_urls = [item['original_url'] for item in redirect_data]
        remove_urls = [item['original_url'] for item in remove_data]

        # Validate sitemap
        expected_validation = self.validate_expected_urls(expected_urls)
        removed_validation = self.validate_removed_urls(remove_urls)

        # Check if original URLs are still in sitemap (they shouldn't be)
        original_validation = self.validate_removed_urls(original_urls)

        return {
            'sitemap_url': self.sitemap_url,
            'total_urls_in_sitemap': len(self.get_sitemap_urls()),
            'expected_urls': expected_validation,
            'removed_urls': removed_validation,
            'original_urls_check': original_validation,
            'fetch_success': bool(self.raw_xml)
        }

    def get_sitemap_stats(self) -> Dict:
        """Get basic statistics about the sitemap."""
        urls = self.get_sitemap_urls()

        # Analyze URL patterns
        paths = []
        for url in urls:
            parsed = urlparse(url)
            paths.append(parsed.path)

        return {
            'total_urls': len(urls),
            'sitemap_url': self.sitemap_url,
            'environment': self.environment,
            'unique_paths': len(set(paths)),
            'sample_urls': urls[:5] if urls else []
        }