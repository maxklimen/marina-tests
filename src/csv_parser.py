"""
CSV parser for handling sitemap test data.
"""
import pandas as pd
import os
from typing import List, Tuple, Dict
from config import Config


class CSVParser:
    """Parser for CSV files containing URL test data."""

    def __init__(self, csv_file_path: str = None):
        """Initialize parser with CSV file path."""
        self.csv_file_path = csv_file_path or Config.get_input_file_path()
        self.data = None
        self.redirect_urls = []
        self.remove_urls = []

    def load_data(self) -> pd.DataFrame:
        """Load CSV data from file."""
        if not os.path.exists(self.csv_file_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_file_path}")

        try:
            self.data = pd.read_csv(self.csv_file_path)
            print(f"✅ Loaded CSV data: {len(self.data)} rows")
            return self.data
        except Exception as e:
            raise Exception(f"Error loading CSV file: {e}")

    def get_redirect_urls(self) -> List[Dict]:
        """Get URLs with 301 redirects that need testing."""
        if self.data is None:
            self.load_data()

        # Filter rows where Status Code is 301
        redirect_rows = self.data[
            self.data.iloc[:, Config.STATUS_CODE_COL] == Config.TARGET_STATUS_CODE
        ]

        redirect_urls = []
        for _, row in redirect_rows.iterrows():
            original_url = row.iloc[Config.ORIGINAL_URL_COL]
            expected_url = row.iloc[Config.EXPECTED_URL_COL]

            # Skip if expected URL is marked for removal
            if str(expected_url).strip().upper() == Config.REMOVE_MARKER:
                continue

            # Clean and validate URLs
            original_url = self._clean_url(original_url)
            expected_url = self._clean_url(expected_url)

            if original_url and expected_url:
                redirect_urls.append({
                    'original_url': original_url,
                    'expected_url': expected_url,
                    'status_code': Config.TARGET_STATUS_CODE
                })

        self.redirect_urls = redirect_urls
        print(f"✅ Found {len(redirect_urls)} URLs with 301 redirects")
        return redirect_urls

    def get_remove_urls(self) -> List[Dict]:
        """Get URLs marked for removal from sitemap."""
        if self.data is None:
            self.load_data()

        # Filter rows where Expected URL is "REMOVE"
        remove_rows = self.data[
            self.data.iloc[:, Config.EXPECTED_URL_COL].astype(str).str.strip().str.upper() == Config.REMOVE_MARKER
        ]

        remove_urls = []
        for _, row in remove_rows.iterrows():
            original_url = row.iloc[Config.ORIGINAL_URL_COL]
            original_url = self._clean_url(original_url)

            if original_url:
                remove_urls.append({
                    'original_url': original_url,
                    'expected_url': Config.REMOVE_MARKER,
                    'status_code': row.iloc[Config.STATUS_CODE_COL]
                })

        self.remove_urls = remove_urls
        print(f"✅ Found {len(remove_urls)} URLs marked for removal")
        return remove_urls

    def get_all_test_data(self) -> Tuple[List[Dict], List[Dict]]:
        """Get both redirect and remove URL data."""
        redirect_urls = self.get_redirect_urls()
        remove_urls = self.get_remove_urls()
        return redirect_urls, remove_urls

    def _clean_url(self, url: str) -> str:
        """Clean and validate URL."""
        if pd.isna(url) or not str(url).strip():
            return ""

        url = str(url).strip()

        # Remove protocol if present (we'll add it back when testing)
        if url.startswith('http://') or url.startswith('https://'):
            url = url.split('://', 1)[1]

        # Handle special cases for external URLs
        if url.startswith('help.californiapsychics.com'):
            return url

        # Ensure URL starts with domain or path
        if not url.startswith('www.californiapsychics.com') and not url.startswith('/'):
            if url.startswith('californiapsychics.com'):
                url = 'www.' + url
            else:
                url = '/' + url

        return url

    def get_statistics(self) -> Dict:
        """Get statistics about the loaded data."""
        if self.data is None:
            self.load_data()

        total_rows = len(self.data)
        redirect_count = len(self.get_redirect_urls())
        remove_count = len(self.get_remove_urls())

        return {
            'total_rows': total_rows,
            'redirect_urls': redirect_count,
            'remove_urls': remove_count,
            'csv_file': self.csv_file_path
        }