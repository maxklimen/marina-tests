#!/usr/bin/env python3
"""
Main script for California Psychics sitemap QA testing.

This script automates the testing of sitemap URLs to validate redirects
and ensure proper URL management for SEO purposes.
"""

import sys
import os
import time
from datetime import datetime

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import Config
from csv_parser import CSVParser
from url_tester import URLTester
from sitemap_handler import SitemapHandler
from reporter import Reporter


def main():
    """Main function to run sitemap QA testing."""
    start_time = time.time()

    # Initialize components
    reporter = Reporter()
    parser = CSVParser()
    tester = URLTester(Config.CURRENT_ENV)
    sitemap_handler = SitemapHandler(Config.CURRENT_ENV)

    try:
        # Print header
        reporter.print_header(Config.CURRENT_ENV)

        # Load and analyze CSV data
        reporter.print_section_header("📊 LOADING TEST DATA")
        print(f"🔄 Loading data from: {Config.get_input_file_path()}")

        redirect_data, remove_data = parser.get_all_test_data()

        # Display statistics
        stats = parser.get_statistics()
        print(f"✅ Data loaded successfully:")
        print(f"   • Total rows in CSV: {stats['total_rows']}")
        print(f"   • URLs with 301 redirects: {stats['redirect_urls']}")
        print(f"   • URLs marked for removal: {stats['remove_urls']}")

        if not redirect_data and not remove_data:
            print("❌ No test data found. Please check your CSV file.")
            return

        # Fetch sitemap first for compliance checking
        reporter.print_section_header("🗺️  FETCHING SITEMAP FOR COMPLIANCE CHECK")
        print("🔄 Fetching sitemap for validation...")

        sitemap_handler.fetch_sitemap()
        sitemap_urls = sitemap_handler.get_sitemap_urls()
        print(f"✅ Sitemap fetched: {len(sitemap_urls)} URLs found")

        # Test redirect URLs with dual verification
        redirect_results = []
        if redirect_data:
            reporter.print_section_header(f"🔄 TESTING REDIRECT URLS ({len(redirect_data)} URLs)")
            print("Testing URL accessibility AND sitemap compliance...\n")

            progress_bar = reporter.create_progress_bar(len(redirect_data), "Testing redirects")

            for i, url_data in enumerate(redirect_data, 1):
                # Test URL accessibility
                result = tester.test_redirect_url(url_data['expected_url'])
                result['original_url'] = url_data['original_url']
                result['test_type'] = 'redirect'

                # Add sitemap compliance checks
                result['url_accessible'] = result['success']  # Rename for clarity
                # Use the prepared URL for sitemap checking (the URL we actually tested)
                result['expected_in_sitemap'] = sitemap_handler.check_url_in_sitemap(result['full_url'])['in_sitemap']
                # For original URL, prepare it the same way to check if it's properly removed
                # Use preserve_trailing_slash=True to distinguish between URLs with/without trailing slashes
                original_prepared = tester._prepare_url(url_data['original_url'])
                result['original_removed'] = not sitemap_handler.check_url_in_sitemap(original_prepared, preserve_trailing_slash=True)['in_sitemap']
                result['sitemap_compliant'] = result['expected_in_sitemap'] and result['original_removed']
                result['success'] = result['url_accessible'] and result['sitemap_compliant']  # Combined success

                # Print individual result with dual criteria
                reporter.print_url_test_result_enhanced(result, i, len(redirect_data))

                redirect_results.append(result)

                # Update progress bar
                if progress_bar:
                    progress_bar.update(1)

                # Small delay to avoid overwhelming the server
                time.sleep(0.1)

            if progress_bar:
                progress_bar.close()

        # Test remove URLs
        remove_results = []
        if remove_data:
            reporter.print_section_header(f"🗑️  TESTING REMOVE URLS ({len(remove_data)} URLs)")
            print("Testing that URLs marked for removal are properly inaccessible...\n")

            progress_bar = reporter.create_progress_bar(len(remove_data), "Testing removals")

            for i, url_data in enumerate(remove_data, 1):
                # Test that the original URL is properly removed/redirected
                result = tester.test_remove_url(url_data['original_url'])
                result['original_url'] = url_data['original_url']
                result['test_type'] = 'remove'

                # Print individual result if verbose
                reporter.print_url_test_result(result, i, len(remove_data))

                remove_results.append(result)

                # Update progress bar
                if progress_bar:
                    progress_bar.update(1)

                # Small delay to avoid overwhelming the server
                time.sleep(0.1)

            if progress_bar:
                progress_bar.close()

        # Analyze sitemap
        sitemap_analysis = None
        try:
            reporter.print_section_header("🗺️  SITEMAP ANALYSIS")
            print("🔄 Fetching and analyzing sitemap...")

            sitemap_analysis = sitemap_handler.get_sitemap_analysis(redirect_data, remove_data)

            if sitemap_analysis['fetch_success']:
                print(f"✅ Sitemap analysis completed:")
                print(f"   • Total URLs in sitemap: {sitemap_analysis['total_urls_in_sitemap']}")

                expected_data = sitemap_analysis.get('expected_urls', {})
                if expected_data:
                    found = expected_data.get('found_in_sitemap', 0)
                    total = expected_data.get('total_expected', 0)
                    missing = len(expected_data.get('missing_from_sitemap', []))
                    print(f"   • Expected URLs found in sitemap: {found}/{total}")
                    if missing > 0:
                        print(f"   • Missing from sitemap: {missing} URLs")

                removed_data = sitemap_analysis.get('removed_urls', {})
                if removed_data:
                    still_present = removed_data.get('still_in_sitemap', 0)
                    if still_present > 0:
                        print(f"   ⚠️  URLs still in sitemap (should be removed): {still_present}")
            else:
                print("❌ Failed to fetch sitemap for analysis")

        except Exception as e:
            print(f"❌ Error during sitemap analysis: {e}")

        # Generate reports
        reporter.print_section_header("📄 GENERATING REPORTS")

        # Save CSV results
        csv_path = reporter.save_csv_results(redirect_results, remove_results)

        # Save HTML report
        html_path = reporter.save_html_report(redirect_results, remove_results, sitemap_analysis)

        # Print summary
        reporter.print_summary(redirect_results, remove_results, sitemap_analysis)

        # Calculate and display total execution time
        total_time = time.time() - start_time
        print(f"⏱️  Total execution time: {total_time:.1f} seconds")

        # Determine exit code based on results
        all_results = redirect_results + remove_results
        failed_tests = sum(1 for r in all_results if not r['success'])

        if failed_tests > 0:
            print(f"\n⚠️  {failed_tests} test(s) failed. Please review the results.")
            return 1
        else:
            print(f"\n🎉 All tests passed successfully!")
            return 0

    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        print("Please ensure the CSV file exists in the 'in/' directory.")
        return 1

    except KeyboardInterrupt:
        print(f"\n\n⏹️  Testing interrupted by user.")
        return 1

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def print_usage():
    """Print usage information."""
    print("""
Usage: python test_sitemap_qa.py

This script tests sitemap URLs for California Psychics QA environment.

Features:
• Tests URLs with 301 redirects to verify Expected URLs return 200
• Validates URLs marked for removal are properly inaccessible
• Analyzes sitemap XML for consistency
• Generates CSV and HTML reports

Output files are saved to the 'output/' directory:
• test_results_YYYY-MM-DD.csv - Detailed test results
• test_report_YYYY-MM-DD.html - Comprehensive report

Configuration:
• Environment: QA (qa-www.californiapsychics.com)
• Input data: in/Psychics.csv
• Timeout: 5 seconds per request
• Retries: 3 attempts for failed requests

For help or issues, check the README.md file.
""")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        print_usage()
        sys.exit(0)

    exit_code = main()
    sys.exit(exit_code)