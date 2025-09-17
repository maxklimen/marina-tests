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

## Development Notes
- Focus on URL testing and validation scripts
- Implement environment switching capability (prod vs QA)
- Design for scalability to handle multiple CSV input files
- Target sitemap: `www.californiapsychics.com/sitemap.xml`