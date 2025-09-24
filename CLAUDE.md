# CLAUDE.md

Developer guidance for Claude Code (claude.ai/code) when working with this codebase.

## Project Overview

QA testing framework for sitemap URL validation with multi-file support, environment isolation, and content-specific sitemap routing.

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
- **Environment Isolation**: Test each environment separately without fallback contamination
- Update sitemaps to use Expected URLs instead of Original URLs
- Remove URLs marked with "REMOVE" in Expected URL column
- Support multiple CSV files with different column structures and content-specific sitemaps
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
1. **File Selection**: Command-line parameters (`--file`, `--all`, `--env`)
2. **CSV Parsing**: Dynamic column mapping based on file type
3. **URL Testing**: HTTP requests with environment-specific URLs
4. **Sitemap Validation**: XML parsing with content-type detection
5. **Environment Isolation**: No fallback contamination between environments
6. **Report Generation**: Unique timestamped output files

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

## 🎉 Multi-Sitemap Architecture (v2.0.0)

### Major Discovery: Content-Specific Sitemaps
The project underwent a significant breakthrough when we discovered that the website uses **multiple dedicated sitemaps** for different content types, not a single monolithic sitemap.

#### Sitemap URL Structure:
- **Main Content**: `/sitemap.xml` (psychic profiles, general content)
- **Horoscope Content**: `/horoscope/sitemap/` (dedicated horoscope sitemap with 248 URLs)
- **Blog Content**: `/blog/sitemap/` (dedicated blog sitemap)

### Implementation Achievement
What initially appeared to be a critical SEO issue (horoscope content missing from sitemaps) was actually a **testing framework limitation**. The solution involved:

1. **Enhanced config.py**: Added `get_sitemap_url(env, csv_file)` method with content-type detection
2. **Dynamic Sitemap Selection**: Framework now automatically selects the correct sitemap based on CSV file type
3. **Massive Improvement**: Horoscope compliance went from **0% to 76.5%** (39/51 URLs found)

### Architecture Implementation
```python
@classmethod
def get_sitemap_url(cls, env=None, csv_file=None):
    """Get sitemap URL for specified environment and CSV file type."""
    base_url = cls.get_base_url(env)

    if csv_file:
        csv_lower = csv_file.lower()
        if 'horoscope' in csv_lower:
            return f'{base_url}/horoscope/sitemap/'
        elif 'blog' in csv_lower:
            return f'{base_url}/blog/sitemap/'

    # Default to main sitemap
    return f'{base_url}/sitemap.xml'
```

## Sitemap Architecture Insights

### QA vs Production Environment Differences
- **QA Main Sitemap**: 1,418 URLs (qa-www.californiapsychics.com/sitemap.xml)
- **Production Main Sitemap**: 1,073 URLs (www.californiapsychics.com/sitemap.xml)
- **Production Horoscope Sitemap**: 248 URLs (www.californiapsychics.com/horoscope/sitemap/)
- **Key Discovery**: Site uses distributed sitemap architecture for content organization

### Content Structure Analysis - UPDATED
- **Articles vs Blog**: Sitemaps use `/articles/` paths, but redirects reference `/blog/` paths
- **✅ Horoscope Content**: Properly found in dedicated `/horoscope/sitemap/` (76.5% compliance)
- **Psychic Profiles**: Present in Production but many missing from QA main sitemap (287 URLs)

### Sitemap Namespace Handling
- **QA Environment**: Uses custom namespace `https://qa-cdn-1.californiapsychics.com/sitemap.xml`
- **Production Environment**: Standard sitemap namespace
- **Parser**: Dynamically detects namespace from root element
- **URL Normalization**: qa-www → www conversion for proper comparison

### Dual Verification Criteria
The testing implements two-stage validation:
1. **URL Accessibility**: Confirms redirect target returns 200 status
2. **Sitemap Compliance**: Verifies URL presence in sitemap XML
3. **Combined Success**: Both criteria must pass for complete validation

### Critical Issues Status - UPDATED
- **✅ Horoscope Gap RESOLVED**: Multi-sitemap implementation revealed 39/51 URLs properly indexed
- **🟡 Path Conflicts**: Blog vs Articles URL structure misalignment (ongoing)
- **🟡 Environment Parity**: QA cannot properly test Production behavior (ongoing)
- **✅ Testing Value**: Tool successfully identified framework limitations vs genuine sitemap gaps

### Technical Evolution
Framework evolved from monolithic sitemap assumption to distributed architecture support with environment isolation for accurate per-environment testing.

## Code Architecture

### Core Components
- **src/config.py**: Environment settings, CSV mappings, sitemap URL routing (lines 80-143)
- **test_sitemap_qa.py**: Main entry point with CLI interface
- **src/sitemap_handler.py**: XML parsing with environment isolation support
- **src/url_tester.py**: HTTP testing with retry logic
- **src/reporter.py**: Output generation (CSV/HTML)

### Key Implementation Details
- **Environment Isolation**: `enable_fallback=False` in SitemapHandler (line 80)
- **Multi-Sitemap Detection**: Content-type based routing in config.py
- **Column Mapping**: Dynamic CSV parsing based on file type
- **Namespace Handling**: XML parser detects sitemap namespace automatically

### Troubleshooting Checklist
- ✅ **RESOLVED**: Environment isolation implemented - no QA→Production fallback contamination
- ✅ **VALIDATED**: Horoscope content achieves 100% compliance with dedicated sitemap
- ✅ **STABLE**: Blog content maintains 81.8% success with main sitemap fallback
- ⚠️ **MONITOR**: Psychic profiles show 59% success (QA/Production sync documented)
- ✅ **VERIFIED**: Test output shows correct sitemap URLs with environment isolation

### Current Performance Status
- **Horoscope QA Testing**: 🎉 **100% success** (51/51 URLs) with dedicated sitemap
- **Blog Testing**: 🟢 **81.8% success** (9/11 URLs) with main sitemap fallback
- **Psychic Testing**: 🟡 **59% success** (201/492 URLs) - QA environment sync needed
- **Environment Isolation**: ✅ **Perfect** - no cross-environment contamination