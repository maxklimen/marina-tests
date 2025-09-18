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
                    'url_accessible', 'url_inaccessible', 'expected_in_sitemap', 'original_removed', 'removed_from_sitemap',
                    'sitemap_compliant', 'fully_removed', 'overall_success', 'error', 'redirect_chain'
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
                        'url_inaccessible': 'N/A',  # Not applicable for redirect URLs
                        'expected_in_sitemap': result.get('expected_in_sitemap', False),
                        'original_removed': result.get('original_removed', False),
                        'removed_from_sitemap': 'N/A',  # Not applicable for redirect URLs
                        'sitemap_compliant': result.get('sitemap_compliant', False),
                        'fully_removed': 'N/A',  # Not applicable for redirect URLs
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
                        'url_accessible': 'N/A',  # Not applicable for removal URLs
                        'url_inaccessible': result.get('url_inaccessible', False),
                        'expected_in_sitemap': result.get('expected_in_sitemap', False),
                        'original_removed': 'N/A',  # Not applicable for removal URLs
                        'removed_from_sitemap': result.get('removed_from_sitemap', False),
                        'sitemap_compliant': result.get('sitemap_compliant', False),
                        'fully_removed': result.get('fully_removed', False),
                        'overall_success': result.get('fully_removed', False),  # Use fully_removed for success
                        'error': result.get('error', ''),
                        'redirect_chain': ','.join(map(str, result.get('redirect_chain', [])))
                    })

            print(f"✅ CSV results saved to: {csv_path}")
            return csv_path

        except Exception as e:
            print(f"❌ Error saving CSV results: {e}")
            return ""

    def _generate_failure_details(self, result: Dict) -> str:
        """Generate detailed failure description for failed tests."""
        details = []
        test_type = result.get('test_type', 'unknown')

        if test_type == 'redirect':
            url_accessible = result.get('url_accessible', False)
            expected_in_sitemap = result.get('expected_in_sitemap', False)
            original_removed = result.get('original_removed', False)

            if not url_accessible:
                status_code = result.get('status_code', 'N/A')
                details.append(f'<span class="badge bg-danger">URL Not Accessible</span> ({status_code})')

            if not expected_in_sitemap:
                details.append('<span class="badge bg-warning">Missing from Sitemap</span>')

            if not original_removed:
                details.append('<span class="badge bg-warning">Original URL Still in Sitemap</span>')

            if result.get('error'):
                details.append(f'<span class="badge bg-secondary">Error</span> {result.get("error")}')

        elif test_type == 'remove':
            url_inaccessible = result.get('url_inaccessible', False)
            removed_from_sitemap = result.get('removed_from_sitemap', False)

            if not url_inaccessible:
                details.append('<span class="badge bg-danger">URL Still Accessible</span>')

            if not removed_from_sitemap:
                details.append('<span class="badge bg-warning">Still in Sitemap</span>')

            if result.get('error'):
                details.append(f'<span class="badge bg-secondary">Error</span> {result.get("error")}')

        return '<div class="failure-details">' + '<br>'.join(details) + '</div>' if details else 'Unknown failure'

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

            # Calculate overall statistics for HTML report
            all_results = redirect_results + remove_results
            passed_tests = sum(1 for r in all_results if r.get('success', False))
            failed_tests = len(all_results) - passed_tests
            success_rate = (passed_tests / len(all_results) * 100) if all_results else 0

            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>California Psychics Sitemap QA Report</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.13.6/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/fixedheader/3.4.0/css/fixedHeader.bootstrap5.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/dataTables.bootstrap5.min.js"></script>
    <script src="https://cdn.datatables.net/fixedheader/3.4.0/js/dataTables.fixedHeader.min.js"></script>
    <style>
        .status-pass {{ background-color: #d1edff !important; }}
        .status-fail {{ background-color: #f8d7da !important; }}
        .status-partial {{ background-color: #fff3cd !important; }}
        .nav-tabs .nav-link.active {{ font-weight: bold; border-bottom: 3px solid #0d6efd; background: white; }}
        .metric-value {{ font-size: 2rem; font-weight: bold; }}
        .metric-label {{ font-size: 0.875rem; color: #6c757d; }}
        .table-responsive {{ max-height: 70vh; }}
        .nav-tabs {{ border-bottom: 2px solid #dee2e6; }}
        .nav-tabs .nav-link {{ border: none; padding: 1rem 1.5rem; font-weight: 500; }}
        .tab-content {{ background: white; border-radius: 0 0 0.375rem 0.375rem; }}
        /* Fixed header styling */
        .dataTables_scrollHead {{
            background: white;
            border-bottom: 2px solid #dee2e6;
        }}
        .dataTables_scrollHeadInner table thead th {{
            background: #f8f9fa;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        /* Fallback sticky headers */
        .sticky-header th {{
            position: sticky;
            top: 0;
            background: #f8f9fa;
            z-index: 10;
            border-bottom: 2px solid #dee2e6;
        }}
        .failure-details {{
            font-size: 0.85rem;
            line-height: 1.3;
        }}
    </style>
</head>
<body class="bg-light">
    <div class="container-fluid py-4">
        <!-- Header -->
        <div class="row mb-4">
            <div class="col">
                <div class="text-center">
                    <h1 class="display-5 mb-2">
                        <i class="fas fa-sitemap text-primary"></i>
                        California Psychics Sitemap QA Report
                    </h1>
                    <p class="text-muted">{datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}</p>
                    <p class="text-muted">Environment: <strong>{Config.CURRENT_ENV.upper()}</strong> ({Config.get_base_url()})</p>
                </div>
            </div>
        </div>

        <!-- Tab Navigation -->
        <ul class="nav nav-tabs mb-0" id="reportTabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="dashboard-tab" data-bs-toggle="tab" data-bs-target="#dashboard" type="button" role="tab">
                    <i class="fas fa-tachometer-alt me-2"></i>Dashboard
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="redirects-tab" data-bs-toggle="tab" data-bs-target="#redirects" type="button" role="tab">
                    <i class="fas fa-exchange-alt me-2"></i>Redirect URLs ({len(redirect_results)})
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="removals-tab" data-bs-toggle="tab" data-bs-target="#removals" type="button" role="tab">
                    <i class="fas fa-trash-alt me-2"></i>Removal URLs ({len(remove_results)})
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="failed-tab" data-bs-toggle="tab" data-bs-target="#failed" type="button" role="tab">
                    <i class="fas fa-exclamation-triangle me-2"></i>Failed Tests ({failed_tests})
                </button>
            </li>
        </ul>

        <!-- Tab Content -->
        <div class="tab-content p-4 bg-white shadow-sm" id="reportTabContent">

            <!-- Dashboard Tab -->
            <div class="tab-pane fade show active" id="dashboard" role="tabpanel">
                <div class="row g-4 mb-4">
                    <div class="col-md-3">
                        <div class="card border-0 shadow-sm h-100">
                            <div class="card-body text-center">
                                <i class="fas fa-list-ol fa-2x text-primary mb-2"></i>
                                <div class="metric-value text-primary">{len(all_results)}</div>
                                <div class="metric-label">Total URLs Tested</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card border-0 shadow-sm h-100">
                            <div class="card-body text-center">
                                <i class="fas fa-check-circle fa-2x text-success mb-2"></i>
                                <div class="metric-value text-success">{passed_tests}</div>
                                <div class="metric-label">Passed Tests</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card border-0 shadow-sm h-100">
                            <div class="card-body text-center">
                                <i class="fas fa-times-circle fa-2x text-danger mb-2"></i>
                                <div class="metric-value text-danger">{failed_tests}</div>
                                <div class="metric-label">Failed Tests</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card border-0 shadow-sm h-100">
                            <div class="card-body text-center">
                                <i class="fas fa-percentage fa-2x text-info mb-2"></i>
                                <div class="metric-value text-info">{success_rate:.1f}%</div>
                                <div class="metric-label">Success Rate</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Quick Stats -->
                <div class="row">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">
                                <h5 class="mb-0"><i class="fas fa-chart-pie me-2"></i>Test Summary</h5>
                            </div>
                            <div class="card-body">
                                <div class="mb-2">
                                    <span class="badge bg-primary me-2">Redirect Tests:</span> {len(redirect_results)}
                                </div>
                                <div class="mb-2">
                                    <span class="badge bg-warning me-2">Removal Tests:</span> {len(remove_results)}
                                </div>
                                <div class="mb-2">
                                    <span class="badge bg-success me-2">Passed:</span> {passed_tests}
                                </div>
                                <div>
                                    <span class="badge bg-danger me-2">Failed:</span> {failed_tests}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header">
                                <h5 class="mb-0"><i class="fas fa-sitemap me-2"></i>Sitemap Analysis</h5>
                            </div>
                            <div class="card-body">"""

            # Add sitemap analysis if available
            if sitemap_analysis and sitemap_analysis.get('fetch_success'):
                expected_data = sitemap_analysis.get('expected_urls', {})
                if expected_data:
                    found = expected_data.get('found_in_sitemap', 0)
                    total = expected_data.get('total_expected', 0)
                    compliance_rate = (found / total * 100) if total > 0 else 0
                    html_content += f"""
                                    <div class="mb-2">
                                        <span class="badge bg-info me-2">Total Sitemap URLs:</span> {sitemap_analysis.get('total_urls_in_sitemap', 0)}
                                    </div>
                                    <div class="mb-2">
                                        <span class="badge bg-success me-2">Expected URLs Found:</span> {found}/{total}
                                    </div>
                                    <div>
                                        <span class="badge bg-primary me-2">Compliance Rate:</span> {compliance_rate:.1f}%
                                    </div>"""
                else:
                    html_content += """
                                    <div class="text-muted">
                                        <i class="fas fa-info-circle me-2"></i>Sitemap analysis not available
                                    </div>"""
            else:
                html_content += """
                                <div class="text-danger">
                                    <i class="fas fa-exclamation-triangle me-2"></i>Sitemap fetch failed
                                </div>"""

            html_content += """
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Redirects Tab -->
            <div class="tab-pane fade" id="redirects" role="tabpanel">
                <div class="mb-3">
                    <div class="alert alert-info">
                        <strong>Legend:</strong>
                        <span class="badge bg-success ms-2">PASS</span> URL accessible AND sitemap compliant
                        <span class="badge bg-warning ms-2">PARTIAL</span> URL accessible but sitemap issues
                        <span class="badge bg-danger ms-2">FAIL</span> URL not accessible or major issues
                    </div>
                </div>
                <div class="table-responsive">
                    <table id="redirectsTable" class="table table-striped table-hover">
                        <thead class="table-dark">
                            <tr>
                                <th>Original URL</th>
                                <th>Expected URL</th>
                                <th>Status</th>
                                <th>Response Time</th>
                                <th>URL Access</th>
                                <th>In Sitemap</th>
                                <th>Original Removed</th>
                                <th>Result</th>
                                <th>Error</th>
                            </tr>
                        </thead>
                        <tbody>"""

            # Add redirect results
            for result in redirect_results:
                url_accessible = result.get('url_accessible', False)
                expected_in_sitemap = result.get('expected_in_sitemap', False)
                original_removed = result.get('original_removed', False)
                overall_success = result.get('success', False)

                if overall_success:
                    row_class = "status-pass"
                    result_badge = '<span class="badge bg-success">PASS</span>'
                elif url_accessible and not (expected_in_sitemap and original_removed):
                    row_class = "status-partial"
                    result_badge = '<span class="badge bg-warning">PARTIAL</span>'
                else:
                    row_class = "status-fail"
                    result_badge = '<span class="badge bg-danger">FAIL</span>'

                url_result = f'<span class="badge bg-success">200</span>' if url_accessible else f'<span class="badge bg-danger">{result.get("status_code", "FAIL")}</span>'
                sitemap_result = '<span class="badge bg-success">Yes</span>' if expected_in_sitemap else '<span class="badge bg-danger">No</span>'
                removed_result = '<span class="badge bg-success">Yes</span>' if original_removed else '<span class="badge bg-danger">No</span>'

                html_content += f"""
                                <tr class="{row_class}">
                                    <td><small>{result.get('original_url', '')}</small></td>
                                    <td><small>{result.get('url', '')}</small></td>
                                    <td>{result.get('status_code', 'N/A')}</td>
                                    <td>{result.get('response_time', 0):.3f}s</td>
                                    <td>{url_result}</td>
                                    <td>{sitemap_result}</td>
                                    <td>{removed_result}</td>
                                    <td>{result_badge}</td>
                                    <td><small>{result.get('error', '')}</small></td>
                                </tr>"""

            html_content += """
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Removals Tab -->
            <div class="tab-pane fade" id="removals" role="tabpanel">
                <div class="mb-3">
                    <div class="alert alert-info">
                        <strong>Removal URL Testing:</strong> These URLs should be inaccessible and removed from sitemap.
                    </div>
                </div>
                <div class="table-responsive">
                    <table id="removalsTable" class="table table-striped table-hover">
                        <thead class="table-dark">
                            <tr>
                                <th>URL to Remove</th>
                                <th>Status Code</th>
                                <th>Response Time</th>
                                <th>URL Access</th>
                                <th>Sitemap Removal</th>
                                <th>Overall Result</th>
                                <th>Error</th>
                            </tr>
                        </thead>
                        <tbody>"""

            # Add removal results with enhanced reporting
            for result in remove_results:
                url_inaccessible = result.get('url_inaccessible', False)
                removed_from_sitemap = result.get('removed_from_sitemap', False)
                fully_removed = result.get('fully_removed', False)

                if fully_removed:
                    row_class = "status-pass"
                    result_badge = '<span class="badge bg-success">FULLY REMOVED</span>'
                else:
                    row_class = "status-fail"
                    result_badge = '<span class="badge bg-danger">STILL PRESENT</span>'

                access_result = '<span class="badge bg-success">Inaccessible</span>' if url_inaccessible else '<span class="badge bg-danger">Still Accessible</span>'
                sitemap_result = '<span class="badge bg-success">Removed</span>' if removed_from_sitemap else '<span class="badge bg-danger">Still in Sitemap</span>'

                html_content += f"""
                                <tr class="{row_class}">
                                    <td><small>{result.get('original_url', '')}</small></td>
                                <td>{result.get('status_code', 'N/A')}</td>
                                <td>{result.get('response_time', 0):.3f}s</td>
                                <td>{access_result}</td>
                                <td>{sitemap_result}</td>
                                <td>{result_badge}</td>
                                <td><small>{result.get('error', '')}</small></td>
                            </tr>"""

            html_content += """
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Failed Tests Tab -->
            <div class="tab-pane fade" id="failed" role="tabpanel">
                <div class="mb-3">
                    <div class="alert alert-danger">
                        <strong>Failed Tests:</strong> These URLs require immediate attention.
                    </div>
                </div>
                <div class="table-responsive">
                    <table id="failedTable" class="table table-striped table-hover">
                        <thead class="table-dark">
                            <tr>
                                <th>URL</th>
                                <th>Test Type</th>
                                <th>Status Code</th>
                                <th>Response Time</th>
                                <th>Failure Details</th>
                                <th>Expected URL</th>
                            </tr>
                        </thead>
                        <tbody>"""

            # Add failed tests
            failed_results = [r for r in all_results if not r.get('success', False)]
            for result in failed_results:
                test_type = result.get('test_type', 'unknown')
                type_badge = f'<span class="badge bg-info">{test_type.upper()}</span>'
                failure_details = self._generate_failure_details(result)

                html_content += f"""
                                <tr class="status-fail">
                                    <td><small>{result.get('original_url', result.get('url', ''))}</small></td>
                                    <td>{type_badge}</td>
                                    <td><span class="badge bg-danger">{result.get('status_code', 'N/A')}</span></td>
                                    <td>{result.get('response_time', 0):.3f}s</td>
                                    <td>{failure_details}</td>
                                    <td><small>{result.get('expected_url', result.get('url', ''))}</small></td>
                                </tr>"""

            html_content += """
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        $(document).ready(function() {{
            // Initialize DataTables with enhanced features and fixed headers
            const tableConfig = {{
                responsive: true,
                pageLength: 25,
                lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
                order: [[0, 'asc']],
                fixedHeader: true,
                scrollY: '60vh',
                scrollCollapse: true,
                columnDefs: [
                    {{ targets: '_all', className: 'text-nowrap' }}
                ],
                dom: '<"row"<"col-sm-6"l><"col-sm-6"f>>' +
                     '<"row"<"col-sm-12"tr>>' +
                     '<"row"<"col-sm-5"i><"col-sm-7"p>>',
                language: {{
                    search: "Search URLs:",
                    lengthMenu: "Show _MENU_ results per page",
                    info: "Showing _START_ to _END_ of _TOTAL_ URLs",
                    paginate: {{
                        first: "First",
                        last: "Last",
                        next: "Next",
                        previous: "Previous"
                    }}
                }}
            }};

            $('#redirectsTable').DataTable(tableConfig);
            $('#removalsTable').DataTable(tableConfig);
            $('#failedTable').DataTable(tableConfig);

            // Auto-switch to failed tab if there are failures
            if ({failed_tests} > 0) {{
                // Optionally highlight the failed tab
                $('#failed-tab').addClass('text-danger');
            }}

            // Enhanced tooltips
            $('[data-bs-toggle="tooltip"]').tooltip();
        }});
    </script>
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