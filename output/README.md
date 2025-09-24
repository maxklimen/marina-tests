# Test Output Directory

This directory contains the generated test reports from the QA sitemap testing tool.

## QA Test Results (2025-09-24) - Environment Isolation Implementation

Latest QA testing results with environment isolation breakthrough:

### Blog Content (11 URLs)
- `test_results_Blog_2025-09-24.csv` - CSV results: 81.8% success (9/11)
- `test_report_Blog_2025-09-24.html` - HTML report with main sitemap validation

### Horoscope Content (51 URLs)
- `test_results_Horoscope_2025-09-24.csv` - CSV results: 100% success (51/51) 🎉
- `test_report_Horoscope_2025-09-24.html` - HTML report with dedicated sitemap validation

### Psychic Profiles (492 URLs)
- `test_results_Psychics_2025-09-24.csv` - CSV results: 59% success (201/492)
- `test_report_Psychics_2025-09-24.html` - HTML report showing QA/Production sync status

## File Formats

### CSV Results (`test_results_YYYY-MM-DD.csv`)
- Excel-compatible format
- Detailed results for each URL tested
- Includes status codes, response times, errors
- Perfect for filtering and analysis

### HTML Reports (`test_report_YYYY-MM-DD.html`)
- Professional visual report
- Summary statistics with charts
- Color-coded pass/fail results
- Ready to share with stakeholders

## Key Achievement: Environment Isolation

**Major Breakthrough (2025-09-24)**: Implemented environment isolation by disabling QA→Production fallback contamination. This revealed the true QA environment state:

- **Horoscope content**: Improved from 0% → 100% compliance
- **Previously**: QA timeout caused fallback to Production sitemap (false results)
- **Now**: Accurate per-environment testing without cross-contamination

## Usage

Generate new reports for specific files:
```bash
python3 test_sitemap_qa.py --file Blog.csv          # Single file
python3 test_sitemap_qa.py --all                    # All files
python3 test_sitemap_qa.py --all --env qa           # QA environment
python3 test_sitemap_qa.py --all --env prod         # Production environment
```

Reports are automatically timestamped to avoid conflicts.