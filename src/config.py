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

    # CSV column mappings for different files (0-based indices)
    CSV_COLUMN_MAPPINGS = {
        'Psychics.csv': {
            'original_url': 0,  # Column 1: Original Url
            'status_code': 3,   # Column 4: Status Code
            'expected_url': 60, # Column 61: Expected URL
            'redirect_url_column': 'Expected URL'  # Column name for redirect URLs
        },
        'Blog.csv': {
            'original_url': 0,  # Column 1: Original Url
            'status_code': 3,   # Column 4: Status Code
            'expected_url': 60, # Column 61: Redirect URL (0-based index 60)
            'redirect_url_column': 'Redirect URL'  # Column name for redirect URLs
        },
        'Horoscope.csv': {
            'original_url': 0,  # Column 1: Original Url
            'status_code': 3,   # Column 4: Status Code
            'expected_url': 63, # Column 64: Expected URL (0-based index 63)
            'redirect_url_column': 'Expected URL'  # Column name for redirect URLs
        }
    }

    # Legacy column indices for backward compatibility
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
    def get_input_file_path(cls, csv_file=None):
        """Get full path to input CSV file."""
        csv_file = csv_file or cls.CSV_FILE
        return os.path.join(cls.INPUT_DIR, csv_file)

    @classmethod
    def get_column_mapping(cls, csv_file=None):
        """Get column mapping for specified CSV file."""
        csv_file = csv_file or cls.CSV_FILE
        return cls.CSV_COLUMN_MAPPINGS.get(csv_file, cls.CSV_COLUMN_MAPPINGS['Psychics.csv'])

    @classmethod
    def set_csv_file(cls, csv_file):
        """Set the current CSV file to use."""
        cls.CSV_FILE = csv_file

    @classmethod
    def get_output_file_path(cls, filename):
        """Get full path to output file."""
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        return os.path.join(cls.OUTPUT_DIR, filename)

    @classmethod
    def get_results_csv_path(cls, csv_file=None):
        """Get full path to results CSV file."""
        filename = cls.get_results_filename(csv_file)
        return cls.get_output_file_path(filename)

    @classmethod
    def get_report_html_path(cls, csv_file=None):
        """Get full path to HTML report file."""
        filename = cls.get_report_filename(csv_file)
        return cls.get_output_file_path(filename)

    @classmethod
    def get_results_filename(cls, csv_file=None):
        """Get results CSV filename with CSV file identifier."""
        csv_file = csv_file or cls.CSV_FILE
        csv_name = csv_file.replace('.csv', '')
        return f'test_results_{csv_name}_{cls.TIMESTAMP}.csv'

    @classmethod
    def get_report_filename(cls, csv_file=None):
        """Get HTML report filename with CSV file identifier."""
        csv_file = csv_file or cls.CSV_FILE
        csv_name = csv_file.replace('.csv', '')
        return f'test_report_{csv_name}_{cls.TIMESTAMP}.html'