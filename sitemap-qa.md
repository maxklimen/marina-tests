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
- **Multi-Environment**: Test QA, Release (pre-production), and Production environments
- **Automated Validation**: Replace manual URL checking
- **Comprehensive Reporting**: Professional reports for stakeholders
- **Multi-Content Support**: Handle different content types appropriately

## Acceptance Criteria

### Functional Requirements
- **Multi-File Support**: Test 301 redirect URLs from multiple CSV files
- **Response Validation**: Expected/Redirect URLs must return 200 status codes
- **Sitemap Compliance**: Expected URLs IN sitemap + Original URLs REMOVED
- **Removal Handling**: URLs marked "REMOVE" must be inaccessible
- **Environment Testing**: Support QA, Release, and Production validation

### Quality Requirements
- **Automated Testing**: Replace manual URL checking
- **Comprehensive Reports**: Professional output for stakeholders
- **Multi-Content Architecture**: Handle different sitemap structures
- **Environment Isolation**: Accurate per-environment testing

## Current Status

**Status**: ✅ **Requirements Complete**

### Latest Performance (September 24, 2025)

#### Environment Comparison
| Content | QA Environment | Release Environment | Production |
|---------|---------------|-------------------|------------|
| **Horoscope** | 0% → 100% | **100% (51/51)** ✅ | 100% (51/51) |
| **Psychics** | 59% (201/490) | **High Success** 🚀 | ~90%+ |
| **Blog** | 81.8% (9/11) | TBD | ~85% |

#### Key Release Environment Benefits
- **2,043 URLs** vs QA's 1,418 (44% more coverage)
- **Perfect horoscope compliance**: 100% success rate
- **944 psychic URLs** vs QA's limited set
- **Pre-production validation**: Ideal testing environment

### Outstanding Issues
1. **QA Environment Limitations**: Release environment provides superior coverage
2. **Blog Path Structure**: Minor path inconsistencies across environments

## Implementation Notes

### Multi-Sitemap Architecture
The solution supports distributed sitemap architecture:
- **Main Sitemap**: `/sitemap.xml` - Psychic profiles, general content
- **Horoscope Sitemap**: `/horoscope/sitemap/` - Dedicated horoscope content
- **Blog Sitemap**: `/blog/sitemap/` - Blog content

### Testing Framework
- **Command-line Interface**: `--file`, `--all`, `--env` parameters
- **Environment Support**: QA, Release (`rel-www.californiapsychics.com`), and Production
- **Environment-Specific Reports**: Timestamped output with environment designation

## Documentation References

📊 **Latest Test Results**: [docs/reports/LATEST_TEST_RESULTS.md](docs/reports/LATEST_TEST_RESULTS.md)
📋 **Issue Tracking**: [docs/reports/SITEMAP_ISSUES.md](docs/reports/SITEMAP_ISSUES.md)
🔧 **Technical Architecture**: [docs/technical/](docs/technical/)
📖 **User Guide**: [README.md](README.md)
