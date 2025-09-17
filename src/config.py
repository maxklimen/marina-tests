"""
Configuration settings for sitemap QA testing.
"""
import os
from datetime import datetime


class Config:
    """Configuration class for sitemap testing."""

    # Environment settings
    ENVIRONMENTS = {
        'qa': 'qa-www.californiapsychics.com',
        'prod': 'www.californiapsychics.com'
    }

    # Default environment for testing
    CURRENT_ENV = 'qa'

    # Request settings
    REQUEST_TIMEOUT = 5  # seconds
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds between retries

    # File paths
    INPUT_DIR = 'in'
    OUTPUT_DIR = 'output'
    CSV_FILE = 'Psychics.csv'

    # CSV column indices (0-based)
    ORIGINAL_URL_COL = 0  # Column 1: Original Url
    STATUS_CODE_COL = 3   # Column 4: Status Code
    EXPECTED_URL_COL = 60 # Column 61: Expected URL

    # Testing parameters
    TARGET_STATUS_CODE = 301
    EXPECTED_RESPONSE_CODE = 200
    REMOVE_MARKER = 'REMOVE'

    # Output settings
    TIMESTAMP = datetime.now().strftime('%Y-%m-%d')
    RESULTS_CSV = f'test_results_{TIMESTAMP}.csv'
    REPORT_HTML = f'test_report_{TIMESTAMP}.html'

    # Display settings
    ENABLE_COLORS = True
    SHOW_PROGRESS = True
    VERBOSE = True

    @classmethod
    def get_base_url(cls, env=None):
        """Get base URL for specified environment."""
        env = env or cls.CURRENT_ENV
        domain = cls.ENVIRONMENTS.get(env, cls.ENVIRONMENTS['qa'])
        return f'https://{domain}'

    @classmethod
    def get_sitemap_url(cls, env=None):
        """Get sitemap URL for specified environment."""
        base_url = cls.get_base_url(env)
        return f'{base_url}/sitemap.xml'

    @classmethod
    def get_input_file_path(cls):
        """Get full path to input CSV file."""
        return os.path.join(cls.INPUT_DIR, cls.CSV_FILE)

    @classmethod
    def get_output_file_path(cls, filename):
        """Get full path to output file."""
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        return os.path.join(cls.OUTPUT_DIR, filename)

    @classmethod
    def get_results_csv_path(cls):
        """Get full path to results CSV file."""
        return cls.get_output_file_path(cls.RESULTS_CSV)

    @classmethod
    def get_report_html_path(cls):
        """Get full path to HTML report file."""
        return cls.get_output_file_path(cls.REPORT_HTML)