# AFL.com.au RSS Feed Generator - Comprehensive Test Checklist

This document provides a comprehensive list of tests that, when passed, indicate the AFL.com.au RSS Feed Generator is working perfectly. These tests cover all components and functionality of the application, including edge cases and error handling.

## 1. Configuration System Tests

### Configuration Loading Tests
- [ ] Test loading a valid configuration file
- [ ] Test loading a configuration file with missing filters section
- [ ] Test loading a configuration file with empty filter lists
- [ ] Test loading a configuration file with only URL patterns
- [ ] Test loading a configuration file with only title keywords
- [ ] Test behavior when config file doesn't exist (should create default)
- [ ] Test behavior when config file is corrupt/invalid YAML
- [ ] Test behavior when config file has unexpected structure
- [ ] Test loading configuration with UTF-8 special characters

### Filtering Logic Tests
- [ ] Test URL filtering with exact match patterns
- [ ] Test URL filtering with substring patterns
- [ ] Test URL filtering with multiple patterns
- [ ] Test URL filtering with no patterns
- [ ] Test URL filtering with empty URL
- [ ] Test URL filtering with case sensitivity
- [ ] Test title filtering with exact match keywords
- [ ] Test title filtering with substring keywords
- [ ] Test title filtering with multiple keywords
- [ ] Test title filtering with no keywords
- [ ] Test title filtering with empty title
- [ ] Test title filtering with case sensitivity
- [ ] Test combined filtering (both URL and title)
- [ ] Test filtering with articles missing fields

## 2. Web Scraper Tests

### HTTP Request Tests
- [ ] Test successful page retrieval
- [ ] Test handling of HTTP 404 errors
- [ ] Test handling of HTTP 500 errors
- [ ] Test handling of connection timeouts
- [ ] Test handling of connection errors
- [ ] Test handling of invalid URLs
- [ ] Test request includes proper user-agent
- [ ] Test request respects timeout settings

### HTML Parsing Tests
- [ ] Test parsing of valid HTML with articles
- [ ] Test parsing of HTML with no articles
- [ ] Test parsing of empty HTML
- [ ] Test parsing of malformed HTML
- [ ] Test extraction of article titles
- [ ] Test extraction of article URLs
- [ ] Test extraction of article descriptions
- [ ] Test extraction of article publication dates
- [ ] Test handling of articles with missing titles
- [ ] Test handling of articles with missing URLs
- [ ] Test handling of articles with missing descriptions
- [ ] Test handling of articles with missing dates
- [ ] Test parsing with varied HTML structures
- [ ] Test parsing of non-standard date formats

### Pagination Tests
- [ ] Test extraction of pagination links
- [ ] Test pagination with multiple pages
- [ ] Test pagination with no additional pages
- [ ] Test respecting max_pages limit
- [ ] Test handling of unexpected pagination structure
- [ ] Test combining articles from multiple pages
- [ ] Test handling of duplicate articles across pages

## 3. State Management Tests

### State Loading Tests
- [ ] Test loading a valid state file
- [ ] Test behavior when state file doesn't exist
- [ ] Test behavior when state file is corrupt/invalid JSON
- [ ] Test loading a state file with no articles
- [ ] Test loading a state file with unexpected structure
- [ ] Test initialization of new state

### Article Tracking Tests
- [ ] Test checking if an article is already scraped (by URL)
- [ ] Test adding a new article to state
- [ ] Test saving state to file
- [ ] Test filtering for new articles only
- [ ] Test handling of duplicate URLs with different dates
- [ ] Test handling of articles missing required fields
- [ ] Test state updating with new articles
- [ ] Test state persistence across runs
- [ ] Test state file permissions and access

## 4. Content Filtering Tests

### Time-Based Selection Tests
- [ ] Test checking if an article is recent (within 24 hours)
- [ ] Test checking if an article is old (older than 24 hours)
- [ ] Test filtering a list of articles by recency
- [ ] Test handling of articles with missing dates
- [ ] Test handling of articles with future dates
- [ ] Test with different hour thresholds
- [ ] Test with articles exactly at the time threshold
- [ ] Test proper timezone handling
- [ ] Test date parsing from various formats

### Content-Based Filtering Tests
- [ ] Test filtering articles by URL patterns
- [ ] Test filtering articles by title keywords
- [ ] Test combined filtering (URL, title, and recency)
- [ ] Test filtering with complex patterns and keywords
- [ ] Test filtering when articles are missing fields
- [ ] Test filtering performance with large article sets

## 5. Feed Generator Tests

### Feed Initialization Tests
- [ ] Test creating a new feed with correct metadata
- [ ] Test feed has proper title ("afl.com.au")
- [ ] Test feed has proper link
- [ ] Test feed has proper description
- [ ] Test feed has proper language setting
- [ ] Test feed has other required RSS 2.0 elements

### Article Addition Tests
- [ ] Test adding a complete article to feed
- [ ] Test adding an article with missing title
- [ ] Test adding an article with missing URL
- [ ] Test adding an article with missing description
- [ ] Test adding an article with missing date
- [ ] Test formatting of publication date to RFC 822
- [ ] Test handling of various date formats
- [ ] Test generation of GUID from article URL

### Feed Generation and Saving Tests
- [ ] Test generating feed with multiple articles
- [ ] Test generating feed with no articles
- [ ] Test saving feed to XML file
- [ ] Test handling of file writing errors
- [ ] Test XML validity of generated feed
- [ ] Test RSS 2.0 compliance of generated feed
- [ ] Test feed with special characters and HTML entities
- [ ] Test feed can be read by common RSS readers

## 6. Main Application Tests

### Application Flow Tests
- [ ] Test complete flow with valid inputs
- [ ] Test flow with missing configuration
- [ ] Test flow with missing state file
- [ ] Test flow with empty article list
- [ ] Test flow with filtered articles
- [ ] Test flow with no new articles
- [ ] Test logging setup and output
- [ ] Test error handling at each stage
- [ ] Test command-line interface (if any)

### Component Integration Tests
- [ ] Test integration of configuration and filtering
- [ ] Test integration of scraper and filtering
- [ ] Test integration of scraper and state management
- [ ] Test integration of filtering and feed generation
- [ ] Test integration of all components end-to-end
- [ ] Test data structure consistency across components
- [ ] Test error propagation between components

## 7. GitHub Actions Integration Tests

### Workflow Tests
- [ ] Test workflow configuration is valid
- [ ] Test workflow runs on schedule
- [ ] Test workflow runs on manual trigger
- [ ] Test Python setup step
- [ ] Test dependencies installation
- [ ] Test script execution
- [ ] Test git commit and push with changes
- [ ] Test git commit and push with no changes
- [ ] Test error handling in workflow

## 8. End-to-End Tests

### Functionality Tests
- [ ] Test complete application with live AFL.com.au site
- [ ] Test filtering out AFLW articles
- [ ] Test including only recent articles
- [ ] Test preventing duplicate articles
- [ ] Test feed output format and content
- [ ] Test feed with real RSS readers
- [ ] Test GitHub Pages hosting of feed
- [ ] Test persistence between runs
- [ ] Test behavior after site structure changes

### Performance Tests
- [ ] Test scraping performance with multiple pages
- [ ] Test filtering performance with large article sets
- [ ] Test memory usage during execution
- [ ] Test execution time for complete process
- [ ] Test behavior under rate limiting or slow connections

### Reliability Tests
- [ ] Test daily execution for a week
- [ ] Test handling of intermittent connection issues
- [ ] Test handling of temporary site changes
- [ ] Test recovery from failed runs
- [ ] Test with various network conditions

## 9. Documentation Tests

### README Tests
- [ ] Verify installation instructions are accurate
- [ ] Verify usage instructions are clear
- [ ] Verify configuration examples work as described
- [ ] Verify troubleshooting section addresses common issues
- [ ] Verify GitHub Actions setup instructions are correct
- [ ] Verify GitHub Pages setup instructions are correct

## 10. Edge Cases and Error Recovery Tests

### Edge Case Tests
- [ ] Test with empty config filters
- [ ] Test with extremely large number of filters
- [ ] Test with extremely long filter strings
- [ ] Test with extremely large number of articles
- [ ] Test with extremely old state file
- [ ] Test with future dates in state file
- [ ] Test with corrupt or partial state file
- [ ] Test with limited disk space
- [ ] Test with limited memory

### Error Recovery Tests
- [ ] Test recovery after network failure
- [ ] Test recovery after disk write error
- [ ] Test recovery after parsing failure
- [ ] Test recovery after partial execution
- [ ] Test recovery after unexpected termination
- [ ] Test handling of unexpected HTML structure
- [ ] Test handling of unexpected date formats
- [ ] Test handling of unexpected URL formats
- [ ] Test handling of invalid article data

## Test Verification Checklist

To confirm the program is working perfectly, verify that:

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] The feed is generated daily at the scheduled time
- [ ] The feed contains only articles from the past 24 hours
- [ ] AFLW articles and other configured filters are excluded
- [ ] No duplicate articles appear in the feed
- [ ] The feed is valid RSS 2.0 and can be read by RSS readers
- [ ] The feed is accessible via GitHub Pages
- [ ] The state file is properly updated after each run
- [ ] Configuration changes take effect without code modifications
- [ ] The application recovers gracefully from errors
- [ ] The application performs well with the real AFL.com.au site
- [ ] The application runs successfully for an extended period
