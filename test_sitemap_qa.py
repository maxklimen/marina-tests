#!/usr/bin/env python3
"""
Main script for California Psychics sitemap QA testing.

This script automates the testing of sitemap URLs to validate redirects
and ensure proper URL management for SEO purposes.
"""

import sys
import os
import time
import argparse
from datetime import datetime

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import Config
from csv_parser import CSVParser
from url_tester import URLTester
from sitemap_handler import SitemapHandler
from reporter import Reporter


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='California Psychics Sitemap QA Testing Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_sitemap_qa.py                    # Test Psychics.csv (default)
  python test_sitemap_qa.py --file Blog.csv    # Test Blog.csv
  python test_sitemap_qa.py --file Horoscope.csv  # Test Horoscope.csv
  python test_sitemap_qa.py --all              # Test all CSV files
        """
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--file', '-f',
                      help='Specify CSV file to test (e.g., Blog.csv, Horoscope.csv)',
                      default='Psychics.csv')
    group.add_argument('--all', '-a',
                      action='store_true',
                      help='Test all CSV files in the input directory')

    parser.add_argument('--env', '-e',
                       choices=['qa', 'prod'],
                       default='qa',
                       help='Environment to test (default: qa)')

    return parser.parse_args()


def get_available_csv_files():
    """Get list of available CSV files in the input directory."""
    input_dir = Config.INPUT_DIR
    if not os.path.exists(input_dir):
        return []

    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    return sorted(csv_files)


def run_test_for_file(csv_file, env='qa'):
    """Run sitemap QA testing for a specific CSV file."""
    start_time = time.time()

    # Set configuration
    Config.set_csv_file(csv_file)
    Config.CURRENT_ENV = env

    # Initialize components
    reporter = Reporter()
    parser = CSVParser(Config.get_input_file_path(csv_file))
    tester = URLTester(Config.CURRENT_ENV)
    sitemap_handler = SitemapHandler(Config.CURRENT_ENV)

    try:
        # Print header with file information
        print(f"\n{'=' * 80}")
        print(f"🧪 TESTING FILE: {csv_file}")
        print(f"{'=' * 80}")
        reporter.print_header(Config.CURRENT_ENV)

        # Load and analyze CSV data
        reporter.print_section_header("📊 LOADING TEST DATA")
        print(f"🔄 Loading data from: {Config.get_input_file_path(csv_file)}")

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

                # Add sitemap check for removal URLs - they should NOT be in sitemap
                prepared_url = tester._prepare_url(url_data['original_url'])
                result['removed_from_sitemap'] = not sitemap_handler.check_url_in_sitemap(prepared_url)['in_sitemap']
                result['url_inaccessible'] = not result['success']  # Should be inaccessible (success=False is good)
                result['expected_in_sitemap'] = False  # Removal URLs should not be in sitemap
                result['sitemap_compliant'] = result['removed_from_sitemap']
                result['fully_removed'] = result['removed_from_sitemap'] and result['url_inaccessible']

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
        csv_path = reporter.save_csv_results(redirect_results, remove_results, csv_file)

        # Save HTML report
        html_path = reporter.save_html_report(redirect_results, remove_results, sitemap_analysis, csv_file)

        # Print summary
        reporter.print_summary(redirect_results, remove_results, sitemap_analysis)

        # Calculate and display total execution time
        total_time = time.time() - start_time
        print(f"⏱️  Total execution time: {total_time:.1f} seconds")

        # Determine exit code based on results
        all_results = redirect_results + remove_results
        failed_tests = sum(1 for r in all_results if not r['success'])

        if failed_tests > 0:
            print(f"\n⚠️  {failed_tests} test(s) failed for {csv_file}. Please review the results.")
            return 1
        else:
            print(f"\n🎉 All tests passed successfully for {csv_file}!")
            return 0

    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        print(f"Please ensure {csv_file} exists in the 'in/' directory.")
        return 1

    except KeyboardInterrupt:
        print(f"\n\n⏹️  Testing interrupted by user.")
        return 1

    except Exception as e:
        print(f"❌ Unexpected error while testing {csv_file}: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main():
    """Main function to run sitemap QA testing."""
    args = parse_arguments()

    if args.all:
        # Test all CSV files
        csv_files = get_available_csv_files()
        if not csv_files:
            print("❌ No CSV files found in the 'in/' directory.")
            return 1

        print(f"🔄 Found {len(csv_files)} CSV file(s): {', '.join(csv_files)}")

        overall_exit_code = 0
        for csv_file in csv_files:
            if csv_file in Config.CSV_COLUMN_MAPPINGS:
                print(f"\n{'=' * 100}")
                print(f"🚀 STARTING TEST FOR: {csv_file}")
                print(f"{'=' * 100}")

                exit_code = run_test_for_file(csv_file, args.env)
                if exit_code != 0:
                    overall_exit_code = exit_code
            else:
                print(f"⚠️  Skipping {csv_file}: No column mapping defined")

        return overall_exit_code
    else:
        # Test single file
        csv_file = args.file

        # Validate file exists
        input_file_path = Config.get_input_file_path(csv_file)
        if not os.path.exists(input_file_path):
            print(f"❌ File not found: {input_file_path}")
            print("Available files:")
            available_files = get_available_csv_files()
            for f in available_files:
                print(f"  • {f}")
            return 1

        # Validate column mapping exists
        if csv_file not in Config.CSV_COLUMN_MAPPINGS:
            print(f"❌ No column mapping defined for {csv_file}")
            print("Supported files:")
            for f in Config.CSV_COLUMN_MAPPINGS.keys():
                print(f"  • {f}")
            return 1

        return run_test_for_file(csv_file, args.env)


def print_usage():
    """Print usage information."""
    print("""
California Psychics Sitemap QA Testing Tool

This script tests sitemap URLs for multiple CSV files with different column structures.

Features:
• Tests URLs with 301 redirects to verify Expected URLs return 200
• Validates URLs marked for removal are properly inaccessible
• Analyzes sitemap XML for consistency
• Generates CSV and HTML reports
• Supports multiple CSV files with different column structures

Usage Examples:
  python test_sitemap_qa.py                    # Test Psychics.csv (default)
  python test_sitemap_qa.py --file Blog.csv    # Test Blog.csv
  python test_sitemap_qa.py --file Horoscope.csv  # Test Horoscope.csv
  python test_sitemap_qa.py --all              # Test all supported CSV files
  python test_sitemap_qa.py --env prod         # Test in production environment

Supported CSV Files:
• Psychics.csv (columns 1, 4, 61)
• Blog.csv (columns 1, 4, 58)
• Horoscope.csv (columns 1, 4, 60)

Output files are saved to the 'output/' directory:
• test_results_YYYY-MM-DD.csv - Detailed test results
• test_report_YYYY-MM-DD.html - Comprehensive report

Configuration:
• Default Environment: QA (qa-www.californiapsychics.com)
• Timeout: 5 seconds per request
• Retries: 3 attempts for failed requests

For help: python test_sitemap_qa.py --help
""")


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)