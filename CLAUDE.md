# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a QA testing repository for sitemap URL validation and redirect management for California Psychics website. The project focuses on testing URLs from CSV data files to ensure proper redirect handling and sitemap maintenance.

## Architecture

### Data Structure
- **Input Data**: CSV files stored in the `in/` directory containing URL analysis data
- **Primary Data File**: `in/Psychics.csv` - contains URL audit data with columns including:
  - `Original Url`: Current URLs in sitemap
  - `Status Code`: HTTP response codes (focus on 301 redirects)
  - `Expected URL`: Target URLs for redirects, or "REMOVE" for URLs to be deleted
  - `Redirect Type`: Type of redirect detected

### Environment Configuration
- **Production**: `www.californiapsychics.com`
- **QA Environment**: `qa-www.californiapsychics.com` (add "qa-" prefix)
- The solution should support easy environment switching

### Key Requirements
- Test URLs with 301 status codes from CSV data
- Verify Expected URLs return 200 status codes
- Update sitemaps to use Expected URLs instead of Original URLs
- Remove URLs marked with "REMOVE" in Expected URL column
- Architecture should be extensible for additional CSV files in `in/` directory

## File Structure
```
.
├── in/                    # Input CSV files for testing
│   └── Psychics.csv      # Primary URL audit data
├── sitemap-qa.md         # QA requirements and acceptance criteria
└── CLAUDE.md            # This file
```

## CSV Data Analysis
Based on analysis of `in/Psychics.csv`:
- **Total URLs with 301 redirects**: 492 entries
- **URLs marked for removal**: 2 entries (marked as "REMOVE" in Expected URL column)
- **Key columns**:
  - Column 1: `Original Url` - URLs currently in sitemap
  - Column 4: `Status Code` - HTTP response codes (filter for 301)
  - Column 61: `Expected URL` - Target URLs for redirects or "REMOVE"

## Testing Workflow
1. **Parse CSV**: Filter 301 status codes from `in/Psychics.csv`
2. **Test Expected URLs**: Verify each Expected URL returns 200 in QA environment
3. **Validate Removals**: Check URLs marked "REMOVE" are inaccessible
4. **Sitemap Comparison**: Fetch and compare actual sitemap against expected state
5. **Generate Reports**: Create transparent output with pass/fail results

## Commands
- **Run QA Tests**: `python test_sitemap_qa.py`
- **Check Dependencies**: `pip install -r requirements.txt`
- **View Results**: Check `output/` directory for reports

## Output Files
- `output/test_results_YYYY-MM-DD.csv` - Failed URLs for Excel review
- `output/test_report_YYYY-MM-DD.html` - Comprehensive HTML report
- Console output with real-time progress and colored results

## Development Notes
- Focus on transparent, user-friendly output for non-technical users
- QA environment testing with "qa-" prefix (qa-www.californiapsychics.com)
- Design for scalability to handle multiple CSV input files
- Target sitemap: `www.californiapsychics.com/sitemap.xml`
- Built to eliminate manual URL checking work