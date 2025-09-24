# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a QA testing repository for sitemap URL validation and redirect management for California Psychics website. The project focuses on testing URLs from CSV data files to ensure proper redirect handling and sitemap maintenance.

## Architecture

### Data Structure
- **Input Data**: Multiple CSV files stored in the `in/` directory containing URL analysis data
- **Supported Data Files**:
  - `in/Psychics.csv` - 492 psychic profile redirects (columns 1, 4, 61)
  - `in/Blog.csv` - 11 blog post redirects (columns 1, 4, 61)
  - `in/Horoscope.csv` - 51 horoscope page redirects (columns 1, 4, 64)
- **Common Columns**:
  - `Original Url`: Current URLs in sitemap
  - `Status Code`: HTTP response codes (focus on 301 redirects)
  - `Expected URL` / `Redirect URL`: Target URLs for redirects, or "REMOVE" for URLs to be deleted
  - `Redirect Type`: Type of redirect detected

### Environment Configuration
- **Production**: `www.californiapsychics.com`
- **QA Environment**: `qa-www.californiapsychics.com` (add "qa-" prefix)
- The solution should support easy environment switching

### Key Requirements
- Test URLs with 301 status codes from multiple CSV data files
- Verify Expected/Redirect URLs return 200 status codes
- Update sitemaps to use Expected URLs instead of Original URLs
- Remove URLs marked with "REMOVE" in Expected URL column
- Support multiple CSV files with different column structures
- Generate unique reports per CSV file to prevent overwrites
- Provide command-line interface for file and environment selection

## File Structure
```
.
├── in/                    # Input CSV files for testing
│   ├── Psychics.csv      # Primary URL audit data (492 redirects)
│   ├── Blog.csv          # Blog URL redirects (11 redirects)
│   └── Horoscope.csv     # Horoscope URL redirects (51 redirects)
├── src/                   # Source code modules
│   ├── config.py         # Configuration and column mappings
│   ├── csv_parser.py     # Dynamic CSV parsing
│   ├── url_tester.py     # URL testing functionality
│   ├── sitemap_handler.py # Sitemap XML processing
│   └── reporter.py       # Report generation with unique filenames
├── output/                # Generated reports (unique per file)
├── test_sitemap_qa.py    # Main script with command-line interface
├── sitemap-qa.md         # QA requirements and acceptance criteria
└── CLAUDE.md            # This file
```

## CSV Data Analysis

### Multi-File Support
The system now supports three CSV files with different column structures:

#### Psychics.csv
- **Total URLs with 301 redirects**: 492 entries
- **URLs marked for removal**: 2 entries (marked as "REMOVE" in Expected URL column)
- **Column structure**: Columns 1, 4, 61 (Expected URL)

#### Blog.csv
- **Total URLs with 301 redirects**: 11 entries
- **URLs marked for removal**: 0 entries
- **Column structure**: Columns 1, 4, 61 (Redirect URL)

#### Horoscope.csv
- **Total URLs with 301 redirects**: 51 entries
- **URLs marked for removal**: 0 entries
- **Column structure**: Columns 1, 4, 64 (Expected URL)

### Common Key Columns
- Column 1: `Original Url` - URLs currently in sitemap
- Column 4: `Status Code` - HTTP response codes (filter for 301)
- Variable: `Expected URL` / `Redirect URL` - Target URLs for redirects or "REMOVE"

## Testing Workflow
1. **Select CSV File**: Choose specific file or test all files with command-line parameters
2. **Parse CSV**: Filter 301 status codes from selected CSV file(s)
3. **Dynamic Column Detection**: Use appropriate column mapping for each CSV file
4. **Test Expected URLs**: Verify each Expected/Redirect URL returns 200 in target environment
5. **Validate Removals**: Check URLs marked "REMOVE" are inaccessible
6. **Sitemap Comparison**: Fetch and compare actual sitemap against expected state
7. **Generate Reports**: Create unique reports per CSV file with transparent output

## Commands

### Basic Usage
- **Run Default Tests**: `python test_sitemap_qa.py` (tests Psychics.csv)
- **Test Specific File**: `python test_sitemap_qa.py --file Blog.csv`
- **Test All Files**: `python test_sitemap_qa.py --all`
- **Check Dependencies**: `pip install -r requirements.txt`

### Environment Selection
- **QA Testing**: `python test_sitemap_qa.py --env qa` (default)
- **Production Testing**: `python test_sitemap_qa.py --env prod`

### Advanced Examples
- **Blog QA**: `python test_sitemap_qa.py --file Blog.csv --env qa`
- **All Files Production**: `python test_sitemap_qa.py --all --env prod`
- **Help**: `python test_sitemap_qa.py --help`

### View Results
- Check `output/` directory for file-specific reports
- Format: `test_results_[filename]_YYYY-MM-DD.csv/html`

## Output Files

### Individual File Reports
- `output/test_results_[filename]_YYYY-MM-DD.csv` - Detailed results for Excel
- `output/test_report_[filename]_YYYY-MM-DD.html` - Comprehensive HTML report
- Console output with real-time progress and colored results

### Example Output Structure
```
output/
├── test_results_Psychics_2025-09-23.csv
├── test_report_Psychics_2025-09-23.html
├── test_results_Blog_2025-09-23.csv
├── test_report_Blog_2025-09-23.html
├── test_results_Horoscope_2025-09-23.csv
└── test_report_Horoscope_2025-09-23.html
```

### Report Features
- **Unique Filenames**: Prevents overwrites when testing multiple files
- **Dual Criteria**: URL accessibility + sitemap compliance validation
- **Enhanced Statistics**: Per-file success rates and detailed failure analysis

## Development Notes
- Focus on transparent, user-friendly output for non-technical users
- QA environment testing with "qa-" prefix (qa-www.californiapsychics.com)
- Design for scalability to handle multiple CSV input files
- Target sitemap: `www.californiapsychics.com/sitemap.xml`
- Built to eliminate manual URL checking work