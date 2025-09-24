# California Psychics - Sitemap QA Testing Tool

Automated testing solution for validating sitemap URLs and redirect management for California Psychics website. This tool eliminates manual URL checking and provides comprehensive reporting for SEO optimization.

## 🎯 Purpose

Automated testing solution for validating sitemap URLs and redirect management for California Psychics website.

### Key Features:
- **✅ Multi-File Support**: Tests Blog.csv, Horoscope.csv, and Psychics.csv
- **✅ Multi-Sitemap Architecture**: Content-specific sitemap routing
- **✅ Environment Testing**: QA and Production environment support
- **✅ Professional Reports**: CSV and HTML output formats

### Sitemap Architecture:
- **Main Content**: `/sitemap.xml` → Psychic profiles, general content
- **Horoscope Content**: `/horoscope/sitemap/` → Dedicated horoscope URLs
- **Blog Content**: `/blog/sitemap/` → Blog-specific content (with fallback)

### What It Does:
- Validates URLs with 301 redirects point to valid destinations (200 status)
- Confirms URLs marked for removal are properly inaccessible
- Verifies sitemap XML reflects the correct URL structure
- Eliminates manual URL checking work

## 📁 Project Structure

```
marina-tests/
├── in/
│   ├── Psychics.csv          # Psychic profiles URL audit data (492 redirects)
│   ├── Blog.csv              # Blog posts URL audit data (11 redirects)
│   └── Horoscope.csv         # Horoscope pages URL audit data (51 redirects)
├── src/
│   ├── config.py             # Configuration and environment settings
│   ├── csv_parser.py         # CSV data parsing and filtering
│   ├── url_tester.py         # URL validation and testing logic
│   ├── sitemap_handler.py    # Sitemap XML fetching and analysis
│   └── reporter.py           # Output formatting and report generation
├── docs/
│   ├── technical/            # Technical implementation documentation
│   │   ├── MULTI_SITEMAP_ARCHITECTURE.md  # v2.0.0 architecture guide
│   │   └── V2_IMPLEMENTATION_STATUS.md    # Production readiness status
│   └── reports/              # Analysis and compliance reports
│       ├── SITEMAP_COMPLIANCE_REPORT.md   # Executive summary
│       └── SITEMAP_ISSUES.md              # Technical issue tracking
├── tests/                    # Unit tests (future enhancement)
├── output/                   # Generated reports and results (unique per file)
├── requirements.txt          # Python dependencies
├── test_sitemap_qa.py        # Main testing script
├── CLAUDE.md                 # Developer documentation
├── CHANGELOG.md              # Release notes and version history
├── sitemap-qa.md             # QA requirements and acceptance criteria
└── README.md                 # This file
```

## 📚 Documentation

### Quick Reference
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes
- **[sitemap-qa.md](sitemap-qa.md)** - QA testing requirements and criteria

### Technical Documentation
- **[Multi-Sitemap Architecture Guide](docs/technical/MULTI_SITEMAP_ARCHITECTURE.md)** - Comprehensive v2.0.0 implementation details
- **[Implementation Status](docs/technical/V2_IMPLEMENTATION_STATUS.md)** - Production readiness assessment

### Test Results & Reports
- **[Latest Test Results](docs/reports/LATEST_TEST_RESULTS.md)** - Current test run analysis (September 24, 2025)
- **[Sitemap Compliance Report](docs/reports/SITEMAP_COMPLIANCE_REPORT.md)** - Executive summary of findings
- **[Technical Issue Tracking](docs/reports/SITEMAP_ISSUES.md)** - Detailed issue status and resolutions

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 📦 What Gets Installed

**Core Testing Libraries:**
- `pandas==2.0.3` - Excel-like data processing for CSV files (handles 1,088 rows efficiently)
- `requests==2.31.0` - HTTP client for testing URLs (handles the 492 redirect tests)
- `lxml==4.9.3` - Fast XML parsing for sitemap.xml files
- `beautifulsoup4==4.12.2` - Robust HTML/XML parsing backup

**User Experience Libraries:**
- `colorama==0.4.6` - Cross-platform colored output (✅ green pass, ❌ red fail)
- `tqdm==4.66.1` - Progress bars for long operations (`[████████░░] 80%`)
- `python-dotenv==1.0.0` - Environment configuration management

*Note: pandas may take 2-3 minutes to compile on first install*

### 2. Run QA Testing

```bash
# Test default file (Psychics.csv)
python test_sitemap_qa.py

# Test specific file
python test_sitemap_qa.py --file Blog.csv
python test_sitemap_qa.py --file Horoscope.csv

# Test all files
python test_sitemap_qa.py --all

# Test in production environment
python test_sitemap_qa.py --file Psychics.csv --env prod
```

### 3. View Results

Check the `output/` directory for file-specific reports:
- `test_results_[filename]_YYYY-MM-DD.csv` - Detailed results for Excel
- `test_report_[filename]_YYYY-MM-DD.html` - Comprehensive report for sharing

## 🎛️ Command-Line Usage

### Available Options

```bash
python test_sitemap_qa.py [OPTIONS]

Options:
  -h, --help            Show help message
  -f FILE, --file FILE  Specify CSV file to test (Blog.csv, Horoscope.csv, Psychics.csv)
  -a, --all             Test all CSV files in the input directory
  -e ENV, --env ENV     Environment to test: qa (default) or prod
```

### Usage Examples

```bash
# Basic usage (tests Psychics.csv in QA)
python test_sitemap_qa.py

# Test specific files
python test_sitemap_qa.py --file Blog.csv
python test_sitemap_qa.py --file Horoscope.csv --env qa

# Test all files at once
python test_sitemap_qa.py --all

# Production environment testing
python test_sitemap_qa.py --file Psychics.csv --env prod
python test_sitemap_qa.py --all --env prod

# Get help
python test_sitemap_qa.py --help
```

## 📊 What Gets Tested

### Supported CSV Files

| File | URLs | Column Structure | Description |
|------|------|------------------|-------------|
| **Psychics.csv** | 492 redirects | Columns 1, 4, 61 (Expected URL) | Psychic profile pages |
| **Blog.csv** | 11 redirects | Columns 1, 4, 61 (Redirect URL) | Blog post redirects |
| **Horoscope.csv** | 51 redirects | Columns 1, 4, 64 (Expected URL) | Horoscope page redirects |

### Test Types

**Redirect URLs (301 Status)**
- **Source**: URLs with status code 301 in CSV files
- **Test**: Verify redirect target returns 200 status code
- **Validation**: Check URL accessibility AND sitemap compliance
- **Environment**: QA (qa-www.californiapsychics.com) or Production

**Remove URLs**
- **Source**: URLs marked "REMOVE" in redirect column
- **Test**: Verify URLs are properly inaccessible (404/redirected)
- **Validation**: Confirm removal from sitemap

**Sitemap Validation**
- **Source**: Live sitemap XML from target environment
- **Test**: Compare against expected URL changes
- **Dual Verification**: Expected URLs IN sitemap + Original URLs REMOVED

## 🎨 Sample Output

```
========================================
🔍 CALIFORNIA PSYCHICS - QA SITEMAP TESTING
========================================
Environment: QA (https://qa-www.californiapsychics.com)
Data Source: in/Psychics.csv
Timestamp: 2025-09-17 14:30:15
========================================

📊 LOADING TEST DATA
--------------------
🔄 Loading data from: in/Psychics.csv
✅ Data loaded successfully:
   • Total rows in CSV: 1000
   • URLs with 301 redirects: 492
   • URLs marked for removal: 2

🔄 TESTING REDIRECT URLS (492 URLs)
-----------------------------------
Testing that Expected URLs return 200 status codes...

[1/492] ✅ /psychics/empath-psychics
        Status: 200 PASS (0.234s)

[2/492] ✅ /about/why-california-psychics
        Status: 200 PASS (0.189s)

[3/492] ❌ help.californiapsychics.com
        Status: 404 FAIL (0.456s)
        Error: Not Found

========================================
📊 TEST SUMMARY
========================================

🔄 Redirect URL Testing:
  ✅ Passed: 489/492 (99.4%)
  ❌ Failed: 3/492 (0.6%)

🗑️  Remove URL Testing:
  ✅ Properly Removed: 2/2

📈 Overall Results:
  Total Tests: 494
  ✅ Passed: 491 (99.4%)
  ❌ Failed: 3 (0.6%)
  ⏱️  Total Time: 124.5s

📁 Output Files:
  CSV Results: output/test_results_2025-09-17.csv
  HTML Report: output/test_report_2025-09-17.html
```

## 🔧 Configuration

### Environment Switching

Use command-line parameters (recommended):
```bash
# QA Environment (default)
python test_sitemap_qa.py --env qa

# Production Environment
python test_sitemap_qa.py --env prod
```

Or edit `src/config.py`:
```python
# Current environment (qa or prod)
CURRENT_ENV = 'qa'

# Available environments
ENVIRONMENTS = {
    'qa': 'qa-www.californiapsychics.com',
    'prod': 'www.californiapsychics.com'
}
```

### CSV File Column Mappings

The tool automatically detects column structures:

```python
CSV_COLUMN_MAPPINGS = {
    'Psychics.csv': {
        'original_url': 0,  # Column 1
        'status_code': 3,   # Column 4
        'expected_url': 60, # Column 61: Expected URL
    },
    'Blog.csv': {
        'original_url': 0,  # Column 1
        'status_code': 3,   # Column 4
        'expected_url': 60, # Column 61: Redirect URL
    },
    'Horoscope.csv': {
        'original_url': 0,  # Column 1
        'status_code': 3,   # Column 4
        'expected_url': 63, # Column 64: Expected URL
    }
}
```

### Testing Parameters

```python
# Request settings
REQUEST_TIMEOUT = 5      # seconds
MAX_RETRIES = 3         # retry attempts
RETRY_DELAY = 1         # seconds between retries

# Display settings
ENABLE_COLORS = True    # colored console output
SHOW_PROGRESS = True    # progress bars
VERBOSE = True          # detailed output
```

## 🏗️ Multi-Sitemap Architecture

### Discovery & Implementation
The v2.0.0 breakthrough came from discovering that California Psychics uses a **distributed sitemap architecture** rather than a single monolithic sitemap. This architectural understanding resolved what initially appeared to be critical SEO issues.

### How It Works
The testing framework now automatically selects the appropriate sitemap based on content type:

```python
# Automatic sitemap selection based on CSV file:
python test_sitemap_qa.py --file Horoscope.csv
# → Tests against: /horoscope/sitemap/

python test_sitemap_qa.py --file Blog.csv
# → Tests against: /blog/sitemap/

python test_sitemap_qa.py --file Psychics.csv
# → Tests against: /sitemap.xml
```

### Current Performance
- **Horoscope Testing**: 100% success with dedicated sitemap
- **Blog Testing**: 81.8% success with main sitemap fallback
- **Psychic Testing**: 59% success (QA environment sync documented)

📊 **Latest Results**: See [docs/reports/LATEST_TEST_RESULTS.md](docs/reports/LATEST_TEST_RESULTS.md) for detailed test run analysis

## 📋 CSV Data Format

The tool supports multiple CSV files with different column structures:

### Psychics.csv
| Column | Index | Description |
|--------|-------|-------------|
| Original Url | 1 | Current URLs in sitemap |
| Status Code | 4 | HTTP response codes (filter for 301) |
| Expected URL | 61 | Target URLs for redirects, or "REMOVE" |

### Blog.csv
| Column | Index | Description |
|--------|-------|-------------|
| Original Url | 1 | Current URLs in sitemap |
| Status Code | 4 | HTTP response codes (filter for 301) |
| Redirect URL | 61 | Target URLs for redirects |

### Horoscope.csv
| Column | Index | Description |
|--------|-------|-------------|
| Original Url | 1 | Current URLs in sitemap |
| Status Code | 4 | HTTP response codes (filter for 301) |
| Expected URL | 64 | Target URLs for redirects, or "REMOVE" |

## 🔍 Understanding Results

### Success Criteria

**Redirect URLs**: ✅ Expected URL returns 200 status code
**Remove URLs**: ✅ Original URL returns 404 or redirects away

### Common Issues

- **404 Errors**: Expected URL doesn't exist or has typos
- **Timeout**: Server is slow or URL is problematic
- **Connection Errors**: Network issues or server problems
- **Still Accessible**: URLs marked for removal are still working

## 🛠️ Troubleshooting

### "CSV file not found"
- Ensure `in/Psychics.csv` exists
- Check file path and permissions

### "Failed to fetch sitemap"
- Verify QA environment is accessible
- Check network connectivity
- Confirm sitemap URL is correct

### High failure rate
- Check if QA environment is properly configured
- Verify CSV data accuracy
- Review network connectivity

### Slow performance
- Adjust `REQUEST_TIMEOUT` in config
- Check server response times
- Consider running during off-peak hours

## 🚀 Adding New CSV Files

1. Place new CSV file in `in/` directory
2. Add column mapping to `Config.CSV_COLUMN_MAPPINGS` in `src/config.py`
3. Ensure CSV has the required columns (Original URL, Status Code, Expected/Redirect URL)
4. Run with: `python test_sitemap_qa.py --file NewFile.csv`

### Example Configuration
```python
'NewFile.csv': {
    'original_url': 0,    # Column index for original URLs
    'status_code': 3,     # Column index for status codes
    'expected_url': 59,   # Column index for redirect URLs
    'redirect_url_column': 'Expected URL'  # Column name
}
```

## ✅ **Status: Production Ready**

The tool has been thoroughly tested with all supported CSV files and environments.

📊 **Current Test Results**: [docs/reports/LATEST_TEST_RESULTS.md](docs/reports/LATEST_TEST_RESULTS.md)
📋 **Business Requirements**: [sitemap-qa.md](sitemap-qa.md)
🔧 **Technical Details**: [docs/technical/](docs/technical/)

## 📋 Known Issues

Two minor issues are documented and monitored:
1. **QA/Production Sync**: Some psychic profiles missing from QA (59% vs expected higher rate)
2. **Blog Path Structure**: Minor path inconsistencies (81.8% success maintained)

📋 **Complete Issue Details**: [docs/reports/SITEMAP_ISSUES.md](docs/reports/SITEMAP_ISSUES.md)

## 📈 Future Enhancements

- [ ] Parallel URL testing for faster execution
- [x] Support for multiple CSV files in one run ✅ **COMPLETED**
- [ ] Combined summary report when using --all flag
- [ ] Email notifications for test results
- [ ] Scheduled testing with cron jobs
- [x] Production environment testing mode ✅ **COMPLETED**
- [ ] Integration with CI/CD pipelines

## 🤝 Support

For issues or questions:
1. Check this README for common solutions
2. Review the generated error messages
3. Examine the detailed CSV output for specific failures
4. Verify CSV data format and content

## 📄 Files Generated

### CSV Results (`output/test_results_[filename]_YYYY-MM-DD.csv`)
Detailed spreadsheet with:
- Test type (redirect/remove)
- Original and expected URLs
- Status codes and response times
- URL accessibility and sitemap compliance
- Dual verification criteria
- Success/failure status
- Error messages

### HTML Report (`output/test_report_[filename]_YYYY-MM-DD.html`)
Professional report with:
- Executive summary with statistics
- Color-coded test results
- Sortable tables
- Enhanced dual criteria validation
- Visual charts and graphs
- Shareable format for stakeholders

### Example Output Files
```
output/
├── test_results_Psychics_2025-09-23.csv
├── test_report_Psychics_2025-09-23.html
├── test_results_Blog_2025-09-23.csv
├── test_report_Blog_2025-09-23.html
├── test_results_Horoscope_2025-09-23.csv
└── test_report_Horoscope_2025-09-23.html
```

---

*This tool was created to automate manual URL checking work and provide transparent, comprehensive testing for sitemap management.*