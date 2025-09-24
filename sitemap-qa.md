# Business Requirements - Sitemap QA Testing

## Problem Statement

California Psychics sitemaps contain outdated URLs that return 301 redirects, negatively impacting SEO performance. The sitemaps need updating to reflect correct URLs and remove redirects.

## Scope

### Content Types
- **Psychics**: 492 URLs with 301 redirects → Update to Expected URLs
- **Blog**: 11 URLs with 301 redirects → Update to Redirect URLs
- **Horoscope**: 51 URLs with 301 redirects → Update to Expected URLs

### Target Sitemaps
- **Main Content**: `www.californiapsychics.com/sitemap.xml`
- **Horoscope**: `www.californiapsychics.com/horoscope/sitemap/`
- **Blog**: `www.californiapsychics.com/blog/sitemap/`

## Business Requirements

### Primary Objectives
1. **Eliminate 301 Redirects**: All sitemap URLs should return 200 status codes
2. **Remove Dead URLs**: URLs marked "REMOVE" must be eliminated from sitemaps
3. **SEO Optimization**: Improve search engine crawling efficiency
4. **Accuracy Validation**: Ensure sitemap reflects actual site structure

### Testing Requirements
- **Multi-Environment**: Test both QA and Production environments
- **Automated Validation**: Replace manual URL checking
- **Comprehensive Reporting**: Professional reports for stakeholders
- **Multi-Content Support**: Handle different content types appropriately

## Acceptance Criteria

### Functional Requirements
- **Multi-File Support**: Test 301 redirect URLs from multiple CSV files
- **Response Validation**: Expected/Redirect URLs must return 200 status codes
- **Sitemap Compliance**: Expected URLs IN sitemap + Original URLs REMOVED
- **Removal Handling**: URLs marked "REMOVE" must be inaccessible
- **Environment Testing**: Support both QA and Production validation

### Quality Requirements
- **Automated Testing**: Replace manual URL checking
- **Comprehensive Reports**: Professional output for stakeholders
- **Multi-Content Architecture**: Handle different sitemap structures
- **Environment Isolation**: Accurate per-environment testing

## Current Status

**Status**: ✅ **Requirements Complete**

### Latest Performance (September 24, 2025)
- **Horoscope**: 100% success with dedicated sitemap
- **Blog**: 81.8% success with main sitemap
- **Psychic**: 59% success (QA environment sync documented)

### Outstanding Issues
1. **QA/Production Sync**: Some psychic profiles missing from QA
2. **Blog Path Structure**: Minor path inconsistencies

## Implementation Notes

### Multi-Sitemap Architecture
The solution supports distributed sitemap architecture:
- **Main Sitemap**: `/sitemap.xml` - Psychic profiles, general content
- **Horoscope Sitemap**: `/horoscope/sitemap/` - Dedicated horoscope content
- **Blog Sitemap**: `/blog/sitemap/` - Blog content

### Testing Framework
- **Command-line Interface**: `--file`, `--all`, `--env` parameters
- **Environment Support**: QA (`qa-www.californiapsychics.com`) and Production
- **Unique Reports**: Timestamped output prevents overwrites

## Documentation References

📊 **Latest Test Results**: [docs/reports/LATEST_TEST_RESULTS.md](docs/reports/LATEST_TEST_RESULTS.md)
📋 **Issue Tracking**: [docs/reports/SITEMAP_ISSUES.md](docs/reports/SITEMAP_ISSUES.md)
🔧 **Technical Architecture**: [docs/technical/](docs/technical/)
📖 **User Guide**: [README.md](README.md)
