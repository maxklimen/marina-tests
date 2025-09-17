###Initial input:

Our current sitemaps for California Psychics, Horoscope, and Blog are outdated. They contain multiple URLs that return a 301 redirect, which negatively impacts SEO. We need to update the sitemaps to reflect the correct URLs and remove all redirects. There are many URLs that are minor syntax updates, and a few URLs that no longer exist which we need to remove.
Acceptance Criteria
Psychics Sitemap
• Review the Psychics tab in the attached Excel file, filter by status code 301
• Update all Original URL entries to their Expected URL
• Apply changes in: www.californiapsychics.com/sitemap.xml


###Important clarifications: 
- We need to test the QA environment first. To access it, we need to add "qa-" before "www". It will be great to design a solution to switch between environments easily
- File for tests inside the "in" folder ; Psychics.csv , we will have another files later there with other links to QA, so it will be great to architect a solution that can be easily modified if necessary.


###Task understanding
- our target to test links that have a 301 Status Code in the file, so sending a request to the Expected URL
- expected response code 200 for Expected URLs - and only updated (Expected URL) should be in the sitemap instead of old ones (Original Url)
- Also, we need to check that URLs have been removed from the sitemap with the value REMOVE in the Expected URL colomn

###QA Environment Implementation Notes
**URL Handling Between Environments:**
- Test data (CSV) contains production URLs (e.g., `www.californiapsychics.com/page`)
- QA testing converts these to QA URLs (e.g., `qa-www.californiapsychics.com/page`)
- QA sitemap contains proper QA URLs with qa-www prefix
- Sitemap validation normalizes qa-www back to www for comparison with test data

**Sitemap Technical Details:**
- QA sitemap uses custom namespace: `https://qa-cdn-1.californiapsychics.com/sitemap.xml`
- Parser detects namespace dynamically from root element
- Standard sitemap namespace fallback for production environment
- Sitemap contains 1,418 URLs in QA environment

**Dual Verification Criteria:**
- **URL Accessibility**: Tests that expected URLs return 200 status
- **Sitemap Compliance**: Verifies expected URLs are IN sitemap AND original URLs are REMOVED
- **Overall Success**: Both criteria must pass for complete validation
