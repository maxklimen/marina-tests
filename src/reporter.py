"""
Reporting functionality for test results and output formatting.
"""
import csv
import json
from datetime import datetime
from typing import List, Dict
from colorama import Fore, Style, init
from tqdm import tqdm
from config import Config

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class Reporter:
    """Reporter class for generating test output and reports."""

    def __init__(self, enable_colors: bool = None):
        """Initialize reporter with color settings."""
        self.enable_colors = enable_colors if enable_colors is not None else Config.ENABLE_COLORS
        self.test_results = []
        self.summary_stats = {}

    def print_header(self, environment: str):
        """Print formatted test header."""
        header = f"""
{'='*60}
🔍 CALIFORNIA PSYCHICS - QA SITEMAP TESTING
{'='*60}
Environment: {environment.upper()} ({Config.get_base_url(environment)})
Data Source: {Config.get_input_file_path()}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}
"""
        print(header)

    def print_section_header(self, title: str):
        """Print formatted section header."""
        print(f"\n{title}")
        print('-' * len(title))

    def print_url_test_result(self, result: Dict, test_number: int, total_tests: int):
        """Print individual URL test result with progress."""
        if not Config.VERBOSE:
            return

        status_symbol = "✅" if result['success'] else "❌"
        status_text = "PASS" if result['success'] else "FAIL"

        url_display = result.get('url', 'Unknown URL')
        response_time = result.get('response_time', 0)
        status_code = result.get('status_code', 'N/A')

        # Color coding
        if self.enable_colors:
            if result['success']:
                status_color = Fore.GREEN
            else:
                status_color = Fore.RED
        else:
            status_color = ""

        print(f"[{test_number}/{total_tests}] {status_symbol} {url_display}")
        print(f"        Status: {status_color}{status_code} {status_text}{Style.RESET_ALL} ({response_time}s)")

        if result.get('error'):
            print(f"        Error: {Fore.RED}{result['error']}{Style.RESET_ALL}")

        if result.get('redirect_chain'):
            print(f"        Redirects: {' → '.join(map(str, result['redirect_chain']))}")

    def print_url_test_result_enhanced(self, result: Dict, test_number: int, total_tests: int):
        """Print enhanced URL test result with dual criteria."""
        if not Config.VERBOSE:
            return

        url_display = result.get('url', 'Unknown URL')
        response_time = result.get('response_time', 0)
        status_code = result.get('status_code', 'N/A')

        # URL accessibility status
        url_accessible = result.get('url_accessible', False)
        url_symbol = "✅" if url_accessible else "❌"
        url_status = "200 OK" if url_accessible else f"{status_code} FAIL"

        # Sitemap compliance status
        sitemap_compliant = result.get('sitemap_compliant', False)
        sitemap_symbol = "✅" if sitemap_compliant else "❌"

        expected_in_sitemap = result.get('expected_in_sitemap', False)
        original_removed = result.get('original_removed', False)

        if expected_in_sitemap and original_removed:
            sitemap_status = "In sitemap, original removed"
        elif expected_in_sitemap:
            sitemap_status = "In sitemap, original still present"
        elif original_removed:
            sitemap_status = "Not in sitemap, original removed"
        else:
            sitemap_status = "Not in sitemap, original still present"

        # Overall status
        overall_success = result.get('success', False)
        overall_symbol = "✅" if overall_success else "❌"
        overall_status = "PASS" if overall_success else "FAIL"

        # Color coding
        if self.enable_colors:
            success_color = Fore.GREEN
            fail_color = Fore.RED
            url_color = success_color if url_accessible else fail_color
            sitemap_color = success_color if sitemap_compliant else fail_color
            overall_color = success_color if overall_success else fail_color
        else:
            url_color = sitemap_color = overall_color = ""

        print(f"[{test_number}/{total_tests}] {url_display}")
        print(f"        URL: {url_symbol} {url_color}{url_status}{Style.RESET_ALL} ({response_time}s)")
        print(f"        Sitemap: {sitemap_symbol} {sitemap_color}{sitemap_status}{Style.RESET_ALL}")
        print(f"        Overall: {overall_symbol} {overall_color}{overall_status}{Style.RESET_ALL}")

        if result.get('error'):
            print(f"        Error: {Fore.RED}{result['error']}{Style.RESET_ALL}")

        if result.get('redirect_chain'):
            print(f"        Redirects: {' → '.join(map(str, result['redirect_chain']))}")

    def print_progress_bar(self, current: int, total: int, description: str = ""):
        """Print progress bar for long operations."""
        if Config.SHOW_PROGRESS and total > 1:
            percentage = (current / total) * 100
            filled = int(50 * current // total)
            bar = '█' * filled + '░' * (50 - filled)
            print(f"\r{description} [{bar}] {current}/{total} ({percentage:.1f}%)", end='', flush=True)
            if current == total:
                print()  # New line when complete

    def create_progress_bar(self, total: int, description: str = "Testing URLs") -> tqdm:
        """Create a tqdm progress bar."""
        if Config.SHOW_PROGRESS:
            return tqdm(total=total, desc=description, unit="url")
        else:
            return None

    def print_summary(self, redirect_results: List[Dict], remove_results: List[Dict],
                     sitemap_analysis: Dict = None):
        """Print comprehensive test summary with dual criteria."""
        print(f"\n{'='*60}")
        print("📊 TEST SUMMARY")
        print(f"{'='*60}")

        # Enhanced redirect URL testing summary
        if redirect_results:
            total_redirects = len(redirect_results)

            # Separate success criteria
            url_accessible = sum(1 for r in redirect_results if r.get('url_accessible', False))
            sitemap_compliant = sum(1 for r in redirect_results if r.get('sitemap_compliant', False))
            overall_success = sum(1 for r in redirect_results if r['success'])

            expected_in_sitemap = sum(1 for r in redirect_results if r.get('expected_in_sitemap', False))
            original_removed = sum(1 for r in redirect_results if r.get('original_removed', False))

            print(f"\n🔄 Redirect URL Testing ({total_redirects} URLs):")
            print(f"  📱 URL Accessibility:     {url_accessible}/{total_redirects} ({(url_accessible/total_redirects)*100:.1f}%)")
            print(f"  🗺️  Sitemap Compliance:    {sitemap_compliant}/{total_redirects} ({(sitemap_compliant/total_redirects)*100:.1f}%)")
            print(f"  ✅ Overall Success:       {overall_success}/{total_redirects} ({(overall_success/total_redirects)*100:.1f}%)")

            print(f"\n🔍 Sitemap Details:")
            print(f"  ✅ Expected URLs in sitemap:   {expected_in_sitemap}/{total_redirects}")
            print(f"  ✅ Original URLs removed:      {original_removed}/{total_redirects}")

            if overall_success < total_redirects:
                failed_accessibility = total_redirects - url_accessible
                failed_sitemap = total_redirects - sitemap_compliant
                print(f"\n⚠️  Issues Found:")
                if failed_accessibility > 0:
                    print(f"  ❌ URLs not accessible: {failed_accessibility}")
                if failed_sitemap > 0:
                    print(f"  ❌ Sitemap non-compliant: {failed_sitemap}")

        # Remove URL testing summary
        if remove_results:
            total_removes = len(remove_results)
            passed_removes = sum(1 for r in remove_results if r['success'])
            failed_removes = total_removes - passed_removes

            print(f"\n🗑️  Remove URL Testing:")
            print(f"  ✅ Properly Removed: {passed_removes}/{total_removes}")
            if failed_removes > 0:
                print(f"  ❌ Still Accessible: {failed_removes}/{total_removes}")

        # Sitemap analysis summary
        if sitemap_analysis:
            print(f"\n🗺️  Sitemap Analysis:")
            print(f"  Total URLs in sitemap: {sitemap_analysis.get('total_urls_in_sitemap', 'N/A')}")

            expected_data = sitemap_analysis.get('expected_urls', {})
            if expected_data:
                found = expected_data.get('found_in_sitemap', 0)
                total = expected_data.get('total_expected', 0)
                print(f"  Expected URLs found: {found}/{total}")

        # Calculate overall statistics
        all_results = (redirect_results or []) + (remove_results or [])
        if all_results:
            total_tests = len(all_results)
            total_passed = sum(1 for r in all_results if r['success'])
            total_failed = total_tests - total_passed

            total_time = sum(r.get('response_time', 0) for r in all_results)

            print(f"\n📈 Overall Results:")
            print(f"  Total Tests: {total_tests}")
            print(f"  ✅ Passed: {total_passed} ({(total_passed/total_tests)*100:.1f}%)")
            if total_failed > 0:
                print(f"  ❌ Failed: {total_failed} ({(total_failed/total_tests)*100:.1f}%)")
            print(f"  ⏱️  Total Time: {total_time:.1f}s")

        print(f"\n📁 Output Files:")
        print(f"  CSV Results: {Config.get_results_csv_path()}")
        print(f"  HTML Report: {Config.get_report_html_path()}")

        print(f"\n{'='*60}")

    def save_csv_results(self, redirect_results: List[Dict], remove_results: List[Dict]) -> str:
        """Save enhanced test results to CSV file with dual criteria."""
        csv_path = Config.get_results_csv_path()

        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'test_type', 'original_url', 'expected_url', 'tested_url',
                    'status_code', 'response_time',
                    'url_accessible', 'expected_in_sitemap', 'original_removed', 'removed_from_sitemap', 'sitemap_compliant',
                    'overall_success', 'error', 'redirect_chain'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                # Write enhanced redirect results
                for result in redirect_results:
                    writer.writerow({
                        'test_type': 'redirect',
                        'original_url': result.get('original_url', ''),
                        'expected_url': result.get('url', ''),
                        'tested_url': result.get('full_url', ''),
                        'status_code': result.get('status_code', ''),
                        'response_time': result.get('response_time', ''),
                        'url_accessible': result.get('url_accessible', False),
                        'expected_in_sitemap': result.get('expected_in_sitemap', False),
                        'original_removed': result.get('original_removed', False),
                        'removed_from_sitemap': 'N/A',  # Not applicable for redirect URLs
                        'sitemap_compliant': result.get('sitemap_compliant', False),
                        'overall_success': result.get('success', False),
                        'error': result.get('error', ''),
                        'redirect_chain': ','.join(map(str, result.get('redirect_chain', [])))
                    })

                # Write remove results
                for result in remove_results:
                    writer.writerow({
                        'test_type': 'remove',
                        'original_url': result.get('original_url', ''),
                        'expected_url': 'REMOVE',
                        'tested_url': result.get('full_url', ''),
                        'status_code': result.get('status_code', ''),
                        'response_time': result.get('response_time', ''),
                        'url_accessible': result.get('url_accessible', False),
                        'expected_in_sitemap': result.get('expected_in_sitemap', False),
                        'original_removed': 'N/A',  # Not applicable for removal URLs
                        'removed_from_sitemap': result.get('removed_from_sitemap', False),
                        'sitemap_compliant': result.get('sitemap_compliant', False),
                        'overall_success': result.get('success', False),
                        'error': result.get('error', ''),
                        'redirect_chain': ','.join(map(str, result.get('redirect_chain', [])))
                    })

            print(f"✅ CSV results saved to: {csv_path}")
            return csv_path

        except Exception as e:
            print(f"❌ Error saving CSV results: {e}")
            return ""

    def save_html_report(self, redirect_results: List[Dict], remove_results: List[Dict],
                        sitemap_analysis: Dict = None) -> str:
        """Save comprehensive HTML report."""
        html_path = Config.get_report_html_path()

        try:
            # Calculate enhanced statistics
            total_redirects = len(redirect_results)
            url_accessible = sum(1 for r in redirect_results if r.get('url_accessible', False))
            sitemap_compliant = sum(1 for r in redirect_results if r.get('sitemap_compliant', False))
            overall_success = sum(1 for r in redirect_results if r['success'])
            total_removes = len(remove_results)
            passed_removes = sum(1 for r in remove_results if r['success'])

            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>California Psychics - QA Sitemap Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
        .container {{ background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; color: #333; border-bottom: 2px solid #007acc; padding-bottom: 20px; }}
        .stats {{ display: flex; justify-content: space-around; margin: 30px 0; }}
        .stat-box {{ text-align: center; padding: 15px; background-color: #f8f9fa; border-radius: 5px; min-width: 120px; }}
        .stat-number {{ font-size: 1.8em; font-weight: bold; color: #007acc; }}
        .success {{ color: #28a745; }}
        .failure {{ color: #dc3545; }}
        .warning {{ color: #ffc107; }}
        .table-container {{ max-height: 600px; overflow-y: auto; margin: 20px 0; border: 1px solid #ddd; border-radius: 5px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #007acc; color: white; position: sticky; top: 0; z-index: 10; box-shadow: 0 2px 2px -1px rgba(0, 0, 0, 0.4); }}
        .pass {{ background-color: #d4edda; }}
        .fail {{ background-color: #f8d7da; }}
        .partial {{ background-color: #fff3cd; }}
        .section {{ margin: 30px 0; }}
        .timestamp {{ color: #666; font-size: 0.9em; }}
        .criteria-section {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 California Psychics - Enhanced QA Sitemap Report</h1>
            <p class="timestamp">Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}</p>
            <p>Environment: <strong>{Config.CURRENT_ENV.upper()}</strong> ({Config.get_base_url()})</p>
        </div>

        <div class="criteria-section">
            <h2>📊 Dual Success Criteria Results</h2>
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number success">{url_accessible}</div>
                    <div>URLs Accessible</div>
                    <div style="font-size: 0.8em;">({(url_accessible/total_redirects)*100:.1f}%)</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number {'success' if sitemap_compliant == total_redirects else 'failure'}">{sitemap_compliant}</div>
                    <div>Sitemap Compliant</div>
                    <div style="font-size: 0.8em;">({(sitemap_compliant/total_redirects)*100:.1f}%)</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number {'success' if overall_success == total_redirects else 'failure'}">{overall_success}</div>
                    <div>Overall Success</div>
                    <div style="font-size: 0.8em;">({(overall_success/total_redirects)*100:.1f}%)</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number {'success' if passed_removes == total_removes else 'failure'}">{passed_removes}</div>
                    <div>URLs Removed</div>
                    <div style="font-size: 0.8em;">({total_removes} total)</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>🔄 Enhanced Redirect URL Testing Results</h2>
            <div class="table-container">
            <table>
                <tr>
                    <th>Original URL</th>
                    <th>Expected URL</th>
                    <th>Status Code</th>
                    <th>Response Time</th>
                    <th>URL Access</th>
                    <th>In Sitemap</th>
                    <th>Original Removed</th>
                    <th>Overall Result</th>
                    <th>Error</th>
                </tr>
"""

            # Add enhanced redirect results
            for result in redirect_results:
                url_accessible = result.get('url_accessible', False)
                expected_in_sitemap = result.get('expected_in_sitemap', False)
                original_removed = result.get('original_removed', False)
                sitemap_compliant = result.get('sitemap_compliant', False)
                overall_success = result.get('success', False)

                if overall_success:
                    row_class = "pass"
                elif url_accessible and not sitemap_compliant:
                    row_class = "partial"
                else:
                    row_class = "fail"

                url_result = "✅ 200" if url_accessible else f"❌ {result.get('status_code', 'FAIL')}"
                sitemap_result = "✅ Yes" if expected_in_sitemap else "❌ No"
                removed_result = "✅ Yes" if original_removed else "❌ No"
                overall_result = "✅ PASS" if overall_success else "❌ FAIL"

                html_content += f"""
                <tr class="{row_class}">
                    <td>{result.get('original_url', '')}</td>
                    <td>{result.get('url', '')}</td>
                    <td>{result.get('status_code', 'N/A')}</td>
                    <td>{result.get('response_time', 0):.3f}s</td>
                    <td>{url_result}</td>
                    <td>{sitemap_result}</td>
                    <td>{removed_result}</td>
                    <td>{overall_result}</td>
                    <td>{result.get('error', '')}</td>
                </tr>
"""

            html_content += """
            </table>
            </div>
        </div>

        <div class="section">
            <h2>🗑️ Remove URL Testing Results</h2>
            <div class="table-container">
            <table>
                <tr>
                    <th>URL to Remove</th>
                    <th>Status Code</th>
                    <th>Response Time</th>
                    <th>Result</th>
                    <th>Error</th>
                </tr>
"""

            # Add remove results
            for result in remove_results:
                row_class = "pass" if result['success'] else "fail"
                result_text = "✅ REMOVED" if result['success'] else "❌ STILL ACCESSIBLE"

                html_content += f"""
                <tr class="{row_class}">
                    <td>{result.get('original_url', '')}</td>
                    <td>{result.get('status_code', 'N/A')}</td>
                    <td>{result.get('response_time', 0):.3f}s</td>
                    <td>{result_text}</td>
                    <td>{result.get('error', '')}</td>
                </tr>
"""

            html_content += """
            </table>
            </div>
        </div>
    </div>
</body>
</html>
"""

            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"✅ HTML report saved to: {html_path}")
            return html_path

        except Exception as e:
            print(f"❌ Error saving HTML report: {e}")
            return ""