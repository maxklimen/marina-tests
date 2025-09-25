"""
Sitemap XML handling for fetching and parsing sitemap data.

Key QA Environment Considerations:
- QA sitemap uses custom namespace: https://qa-cdn-1.californiapsychics.com/sitemap.xml
- QA sitemap contains URLs with qa-www prefix (e.g., qa-www.californiapsychics.com)
- Test data contains production URLs (e.g., www.californiapsychics.com)
- URL normalization handles qa-www -> www conversion for proper comparison

IMPORTANT NOTE: Manual review identified discrepancies in QA sitemap requiring attention.
Current 4.7% compliance rate indicates systematic sitemap updates needed.
See sitemap-qa.md for detailed action items for next session.
"""
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Set
from urllib.parse import urlparse
from config import Config


class SitemapHandler:
    """Handler for sitemap XML operations."""

    def __init__(self, environment: str = None, sitemap_url: str = None, enable_fallback: bool = False):
        """
        Initialize sitemap handler with environment and optional sitemap URL.

        Args:
            environment: Target environment ('qa' or 'prod')
            sitemap_url: Optional explicit sitemap URL
            enable_fallback: If True, allow fallback to production when QA fails (default: False)
                           Setting to False ensures accurate per-environment testing
        """
        self.environment = environment or Config.CURRENT_ENV
        self.sitemap_url = sitemap_url or Config.get_sitemap_url(self.environment)
        self.enable_fallback = enable_fallback
        self.urls = []
        self.raw_xml = None

    def fetch_sitemap(self) -> bool:
        """
        Fetch sitemap XML from the website.

        If enable_fallback is True, will try production fallback when QA fails.
        If enable_fallback is False, will only test the specified environment.
        """
        env_name = "QA" if "qa-" in self.sitemap_url else "Production"
        primary_success = self._try_fetch_sitemap(self.sitemap_url, env_name)

        if primary_success:
            return True

        # Only attempt fallback if explicitly enabled
        if self.enable_fallback and "qa-" in self.sitemap_url:
            print("⚠️  QA sitemap failed, trying production fallback...")
            prod_url = self.sitemap_url.replace('qa-www.', 'www.')
            prod_success = self._try_fetch_sitemap(prod_url, "Production")
            if prod_success:
                print("ℹ️  Using production sitemap for validation")
                return True
            print("❌ Both QA and production sitemaps failed")
        else:
            print(f"❌ {env_name} sitemap failed (fallback disabled for accurate environment testing)")

        return False

    def _try_fetch_sitemap(self, url: str, env_name: str) -> bool:
        """Try to fetch sitemap from a specific URL."""
        try:
            print(f"🔄 Fetching {env_name} sitemap from: {url}")

            response = requests.get(
                url,
                timeout=Config.REQUEST_TIMEOUT,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )

            if response.status_code == 200:
                self.raw_xml = response.text
                print(f"✅ {env_name} sitemap fetched successfully ({len(self.raw_xml)} bytes)")
                return True
            else:
                print(f"❌ Failed to fetch {env_name} sitemap: HTTP {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching {env_name} sitemap: {e}")
            return False

    def parse_sitemap(self) -> List[str]:
        """Parse sitemap XML and extract URLs."""
        if not self.raw_xml:
            if not self.fetch_sitemap():
                return []

        try:
            # Parse XML
            root = ET.fromstring(self.raw_xml)

            # Detect namespace from root element
            namespace_uri = None
            if root.tag.startswith('{'):
                namespace_uri = root.tag[1:root.tag.find('}')]

            # Extract URLs from sitemap
            urls = []

            # Try with detected namespace first
            if namespace_uri:
                namespaces = {'ns': namespace_uri}
                for url_element in root.findall('.//ns:url', namespaces):
                    loc_element = url_element.find('ns:loc', namespaces)
                    if loc_element is not None and loc_element.text:
                        urls.append(loc_element.text.strip())

            # If no URLs found, try standard sitemap namespace
            if not urls:
                namespaces = {
                    'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'
                }
                for url_element in root.findall('.//sitemap:url', namespaces):
                    loc_element = url_element.find('sitemap:loc', namespaces)
                    if loc_element is not None and loc_element.text:
                        urls.append(loc_element.text.strip())

            # If still no URLs found, try without namespace
            if not urls:
                for url_element in root.findall('.//url'):
                    loc_element = url_element.find('loc')
                    if loc_element is not None and loc_element.text:
                        urls.append(loc_element.text.strip())

            self.urls = urls
            print(f"✅ Parsed {len(urls)} URLs from sitemap")
            if namespace_uri:
                print(f"ℹ️  Used namespace: {namespace_uri}")
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

    def normalize_url_for_comparison(self, url: str, preserve_trailing_slash: bool = False) -> str:
        """Normalize URL for comparison purposes."""
        if not url:
            return ""

        # Remove protocol
        normalized = url.replace('https://', '').replace('http://', '')

        # Handle trailing slash (preserve if requested for distinguishing between similar URLs)
        if not preserve_trailing_slash and normalized.endswith('/'):
            normalized = normalized[:-1]

        # Normalize environment prefixes for comparison
        # Convert environment prefixes back to www for comparison since test data uses production URLs
        normalized = normalized.replace('qa-www.californiapsychics.com', 'www.californiapsychics.com')
        normalized = normalized.replace('rel-www.californiapsychics.com', 'www.californiapsychics.com')

        # Convert to lowercase for case-insensitive comparison
        normalized = normalized.lower()

        return normalized

    def check_url_in_sitemap(self, test_url: str, preserve_trailing_slash: bool = False) -> Dict:
        """Check if a URL exists in the sitemap."""
        sitemap_urls = self.get_sitemap_urls()
        normalized_test_url = self.normalize_url_for_comparison(test_url, preserve_trailing_slash)

        # Normalize all sitemap URLs for comparison
        normalized_sitemap_urls = [
            self.normalize_url_for_comparison(url, preserve_trailing_slash) for url in sitemap_urls
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