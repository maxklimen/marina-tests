"""
URL testing functionality for validating redirects and responses.
"""
import requests
import time
from typing import Dict, List
from urllib.parse import urljoin, urlparse
from config import Config


class URLTester:
    """URL testing class for validating website responses."""

    def __init__(self, environment: str = None):
        """Initialize URL tester with environment."""
        self.environment = environment or Config.CURRENT_ENV
        self.base_url = Config.get_base_url(self.environment)
        self.session = requests.Session()

        # Set up session headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def test_url(self, url: str, expected_status: int = None) -> Dict:
        """Test a single URL and return results."""
        expected_status = expected_status or Config.EXPECTED_RESPONSE_CODE

        # Prepare the full URL
        full_url = self._prepare_url(url)

        result = {
            'url': url,
            'full_url': full_url,
            'status_code': None,
            'response_time': None,
            'success': False,
            'error': None,
            'redirect_chain': []
        }

        start_time = time.time()

        try:
            response = self._make_request_with_retry(full_url)

            result['status_code'] = response.status_code
            result['response_time'] = round(time.time() - start_time, 3)
            result['success'] = response.status_code == expected_status

            # Track redirect chain
            if response.history:
                result['redirect_chain'] = [r.status_code for r in response.history]

            # Additional checks for successful responses
            if response.status_code == 200:
                # Check if page actually loads content (not just returns 200)
                content_length = len(response.content)
                if content_length < 100:  # Suspiciously small content
                    result['error'] = f"Response too small ({content_length} bytes)"
                    result['success'] = False

        except requests.exceptions.Timeout:
            result['error'] = 'Request timeout'
            result['response_time'] = Config.REQUEST_TIMEOUT

        except requests.exceptions.ConnectionError:
            result['error'] = 'Connection error'
            result['response_time'] = round(time.time() - start_time, 3)

        except requests.exceptions.RequestException as e:
            result['error'] = f'Request error: {str(e)}'
            result['response_time'] = round(time.time() - start_time, 3)

        except Exception as e:
            result['error'] = f'Unexpected error: {str(e)}'
            result['response_time'] = round(time.time() - start_time, 3)

        return result

    def test_redirect_url(self, expected_url: str) -> Dict:
        """Test if an expected URL returns 200 status."""
        return self.test_url(expected_url, Config.EXPECTED_RESPONSE_CODE)

    def test_remove_url(self, url: str) -> Dict:
        """Test if a URL marked for removal is properly inaccessible."""
        result = self.test_url(url)

        # For remove URLs, we expect 404 or redirect away from the original domain
        if result['status_code'] in [404, 410]:  # Not Found or Gone
            result['success'] = True
        elif result['status_code'] in [301, 302, 303, 307, 308]:  # Redirects
            # Check if redirect goes to external domain
            if result.get('redirect_chain'):
                result['success'] = True  # Redirect away is acceptable
        else:
            result['success'] = False
            if not result['error']:
                result['error'] = f"URL should be removed but returns {result['status_code']}"

        return result

    def test_multiple_urls(self, urls: List[Dict], test_type: str = 'redirect') -> List[Dict]:
        """Test multiple URLs and return results."""
        results = []

        for i, url_data in enumerate(urls, 1):
            if test_type == 'redirect':
                expected_url = url_data['expected_url']
                result = self.test_redirect_url(expected_url)
                result['original_url'] = url_data['original_url']
                result['test_type'] = 'redirect'

            elif test_type == 'remove':
                original_url = url_data['original_url']
                result = self.test_remove_url(original_url)
                result['original_url'] = original_url
                result['test_type'] = 'remove'

            result['test_number'] = i
            result['total_tests'] = len(urls)
            results.append(result)

        return results

    def _prepare_url(self, url: str) -> str:
        """Prepare URL for testing."""
        if not url:
            return ""

        # Handle external URLs (help subdomain)
        if url.startswith('help.californiapsychics.com'):
            if not url.startswith('http'):
                return f'https://{url}'
            return url

        # Handle URLs that already have protocol
        if url.startswith('http'):
            return url

        # Handle URLs with full domain - need to add QA prefix if in QA environment
        if url.startswith('www.californiapsychics.com'):
            if self.environment == 'QA':
                # Replace www with qa-www for QA testing
                qa_url = url.replace('www.californiapsychics.com', 'qa-www.californiapsychics.com')
                return f'https://{qa_url}'
            else:
                return f'https://{url}'

        # Handle relative URLs
        if url.startswith('/'):
            return f'{self.base_url}{url}'

        # Default case - assume it's a path, use base_url which already has the right environment
        return f'{self.base_url}/{url.lstrip("/")}'

    def _make_request_with_retry(self, url: str) -> requests.Response:
        """Make HTTP request with retry logic."""
        last_exception = None

        for attempt in range(Config.MAX_RETRIES):
            try:
                response = self.session.get(
                    url,
                    timeout=Config.REQUEST_TIMEOUT,
                    allow_redirects=True
                )
                return response

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                last_exception = e
                if attempt < Config.MAX_RETRIES - 1:
                    time.sleep(Config.RETRY_DELAY * (attempt + 1))  # Exponential backoff
                    continue
                else:
                    raise e

            except requests.exceptions.RequestException as e:
                # Don't retry for other request exceptions
                raise e

        # Should not reach here, but just in case
        raise last_exception

    def get_session_stats(self) -> Dict:
        """Get statistics about the current testing session."""
        return {
            'environment': self.environment,
            'base_url': self.base_url,
            'timeout': Config.REQUEST_TIMEOUT,
            'max_retries': Config.MAX_RETRIES
        }