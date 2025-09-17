# Test Output Directory

This directory contains the generated test reports from the QA sitemap testing tool.

## Sample Files Included

- `test_results_2025-09-17.csv` - Sample CSV results showing 492 URL tests
- `test_report_2025-09-17.html` - Sample HTML report with visual summary

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

## Usage

New reports are generated each time you run:
```bash
python3 test_sitemap_qa.py
```

Reports are automatically timestamped to avoid conflicts.