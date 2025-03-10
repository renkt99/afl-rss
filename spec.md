# Developer Specification: AFL.com.au RSS Feed Generator

## Project Overview

A scheduled web scraper that generates a standard RSS feed for AFL.com.au news articles, with configurable content filtering capabilities.

## Technical Requirements

### Technology Stack

- **Programming Language:** Python 3.x
- **Key Libraries:**
  - BeautifulSoup4 for HTML parsing
  - feedgen for RSS generation
  - requests for HTTP requests
  - PyYAML for configuration management

### Hosting & Infrastructure

- **Platform:** GitHub Actions for execution
- **Hosting:** GitHub Pages for feed delivery
- **Schedule:** Daily at 12:37 AM AWST (16:37 UTC)
- **Repository Structure:**
  
  ```
  /
  ├── .github/
  │   └── workflows/
  │       └── generate_rss.yml    # GitHub Actions workflow
  ├── src/
  │   ├── scraper.py              # Main scraping logic
  │   ├── feed_generator.py       # RSS feed generation
  │   ├── utils.py                # Helper functions
  │   └── main.py                 # Entry point
  ├── config.yml                  # Configuration file
  ├── previously_scraped.json     # State file
  ├── feed.xml                    # Generated RSS feed
  ├── README.md                   # Documentation
  └── requirements.txt            # Dependencies
  ```

## Functional Requirements

### Core Functionality

1. **Web Scraping:**
   
   - Target URL: https://afl.com.au/news
   - Extract article information: title, URL, description, publication date
   - Handle pagination if necessary to get all recent articles

2. **Content Filtering:**
   
   - Configurable filtering system via config.yml
   - Default filters:
     - Exclude articles with URLs containing "/aflw/"
     - Support for additional keyword filters in titles and URLs
   - Configuration file format:
     
     ```yaml
     filters:
       url_patterns:
         - "/aflw/"
         - "/other-pattern/"
       title_keywords:
         - "unwanted keyword"
     ```

3. **Time-based Selection:**
   
   - Include only articles published within the last 24 hours
   - On first run, only include articles from the past 24 hours

4. **Duplicate Prevention:**
   
   - Maintain state between runs via previously_scraped.json
   - Store article URLs and publication dates
   - Skip articles already present in the state file
   - Update and commit state file after each successful run

5. **RSS Feed Generation:**
   
   - Format: Standard RSS 2.0
   - Feed Title: "afl.com.au"
   - Include for each item:
     - Title
     - Link (URL)
     - Description (summary)
     - Publication date

### GitHub Actions Workflow

```yaml
name: Generate AFL RSS Feed

on:
  schedule:
    # Run at 16:37 UTC (12:37 AM AWST)
    - cron: '37 16 * * *'
  workflow_dispatch:  # Allow manual trigger

jobs:
  generate-feed:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Generate RSS feed
        run: python src/main.py

      - name: Configure Git
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com

      - name: Commit and push changes
        run: |
          git add feed.xml previously_scraped.json
          git commit -m "Update RSS feed" || echo "No changes to commit"
          git push
```

## Technical Implementation Details

### Scraper Module

- Use requests library for fetching the AFL news page
- Use BeautifulSoup for parsing HTML content
- Extract article information from the page structure
- Handle potential changes in page structure gracefully

### Feed Generator Module

- Use feedgen library to create standard RSS 2.0 feed
- Set feed metadata (title, link, description)
- Add extracted articles as items in the feed
- Format dates according to RFC 822 standard

### State Management

- Store previously scraped article URLs in JSON format
- Structure:
  
  ```json
  {
    "last_run": "2025-03-10T12:37:00+08:00",
    "articles": [
      {
        "url": "https://afl.com.au/news/article-1",
        "published": "2025-03-09T15:30:00+08:00"
      },
      ...
    ]
  }
  ```
- On each run:
  1. Load previously_scraped.json
  2. Filter out already scraped articles
  3. Update with newly scraped articles
  4. Save updated state

### GitHub Pages Setup

- Enable GitHub Pages in repository settings
- Configure to serve from the main branch
- Feed will be accessible at: https://[username].github.io/[repo-name]/feed.xml

## Error Handling

- Implement robust error handling for website changes
- Log errors to standard output (visible in GitHub Actions logs)
- Continue operation on non-critical errors
- Ensure the workflow doesn't fail completely if scraping encounters issues

## Testing Plan

1. **Unit Tests:**
   
   - Test filter logic with various inputs
   - Test state management functions
   - Test feed generation with mock data

2. **Integration Tests:**
   
   - Test end-to-end flow with sample HTML
   - Verify filtering works as expected with real data

3. **Manual Tests:**
   
   - Initial run on real website
   - Subscribe to feed in RSS reader
   - Verify articles match expected filters

## Implementation Timeline (Suggested)

1. Set up repository structure and GitHub Actions workflow
2. Implement scraper for AFL.com.au
3. Implement filtering logic
4. Develop RSS feed generation
5. Add state management to prevent duplicates
6. Test and refine
7. Set up GitHub Pages for hosting
8. Create documentation

## Acceptance Criteria

- RSS feed is generated daily at 12:37 AM AWST
- Feed contains only articles from the past 24 hours
- AFLW articles and other configured filters are excluded
- No duplicate articles appear in the feed
- Feed is accessible via GitHub Pages
- Configuration changes don't require code modifications

This specification provides all necessary details for a developer to implement the AFL.com.au RSS feed generator with configurable filtering capabilities.# Developer Specification: AFL.com.au RSS Feed Generator

## Project Overview

A scheduled web scraper that generates a standard RSS feed for AFL.com.au news articles, with configurable content filtering capabilities.

## Technical Requirements

### Technology Stack

- **Programming Language:** Python 3.x
- **Key Libraries:**
  - BeautifulSoup4 for HTML parsing
  - feedgen for RSS generation
  - requests for HTTP requests
  - PyYAML for configuration management

### Hosting & Infrastructure

- **Platform:** GitHub Actions for execution
- **Hosting:** GitHub Pages for feed delivery
- **Schedule:** Daily at 12:37 AM AWST (16:37 UTC)
- **Repository Structure:**
  
  ```
  /
  ├── .github/
  │   └── workflows/
  │       └── generate_rss.yml    # GitHub Actions workflow
  ├── src/
  │   ├── scraper.py              # Main scraping logic
  │   ├── feed_generator.py       # RSS feed generation
  │   ├── utils.py                # Helper functions
  │   └── main.py                 # Entry point
  ├── config.yml                  # Configuration file
  ├── previously_scraped.json     # State file
  ├── feed.xml                    # Generated RSS feed
  ├── README.md                   # Documentation
  └── requirements.txt            # Dependencies
  ```

## Functional Requirements

### Core Functionality

1. **Web Scraping:**
   
   - Target URL: https://afl.com.au/news
   - Extract article information: title, URL, description, publication date
   - Handle pagination if necessary to get all recent articles

2. **Content Filtering:**
   
   - Configurable filtering system via config.yml
   - Default filters:
     - Exclude articles with URLs containing "/aflw/"
     - Support for additional keyword filters in titles and URLs
   - Configuration file format:
     
     ```yaml
     filters:
       url_patterns:
         - "/aflw/"
         - "/other-pattern/"
       title_keywords:
         - "unwanted keyword"
     ```

3. **Time-based Selection:**
   
   - Include only articles published within the last 24 hours
   - On first run, only include articles from the past 24 hours

4. **Duplicate Prevention:**
   
   - Maintain state between runs via previously_scraped.json
   - Store article URLs and publication dates
   - Skip articles already present in the state file
   - Update and commit state file after each successful run

5. **RSS Feed Generation:**
   
   - Format: Standard RSS 2.0
   - Feed Title: "afl.com.au"
   - Include for each item:
     - Title
     - Link (URL)
     - Description (summary)
     - Publication date

### GitHub Actions Workflow

```yaml
name: Generate AFL RSS Feed

on:
  schedule:
    # Run at 16:37 UTC (12:37 AM AWST)
    - cron: '37 16 * * *'
  workflow_dispatch:  # Allow manual trigger

jobs:
  generate-feed:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Generate RSS feed
        run: python src/main.py

      - name: Configure Git
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com

      - name: Commit and push changes
        run: |
          git add feed.xml previously_scraped.json
          git commit -m "Update RSS feed" || echo "No changes to commit"
          git push
```

## Technical Implementation Details

### Scraper Module

- Use requests library for fetching the AFL news page
- Use BeautifulSoup for parsing HTML content
- Extract article information from the page structure
- Handle potential changes in page structure gracefully

### Feed Generator Module

- Use feedgen library to create standard RSS 2.0 feed
- Set feed metadata (title, link, description)
- Add extracted articles as items in the feed
- Format dates according to RFC 822 standard

### State Management

- Store previously scraped article URLs in JSON format
- Structure:
  
  ```json
  {
    "last_run": "2025-03-10T12:37:00+08:00",
    "articles": [
      {
        "url": "https://afl.com.au/news/article-1",
        "published": "2025-03-09T15:30:00+08:00"
      },
      ...
    ]
  }
  ```
- On each run:
  1. Load previously_scraped.json
  2. Filter out already scraped articles
  3. Update with newly scraped articles
  4. Save updated state

### GitHub Pages Setup

- Enable GitHub Pages in repository settings
- Configure to serve from the main branch
- Feed will be accessible at: https://[username].github.io/[repo-name]/feed.xml

## Error Handling

- Implement robust error handling for website changes
- Log errors to standard output (visible in GitHub Actions logs)
- Continue operation on non-critical errors
- Ensure the workflow doesn't fail completely if scraping encounters issues

## Testing Plan

1. **Unit Tests:**
   
   - Test filter logic with various inputs
   - Test state management functions
   - Test feed generation with mock data

2. **Integration Tests:**
   
   - Test end-to-end flow with sample HTML
   - Verify filtering works as expected with real data

3. **Manual Tests:**
   
   - Initial run on real website
   - Subscribe to feed in RSS reader
   - Verify articles match expected filters

## Implementation Timeline (Suggested)

1. Set up repository structure and GitHub Actions workflow
2. Implement scraper for AFL.com.au
3. Implement filtering logic
4. Develop RSS feed generation
5. Add state management to prevent duplicates
6. Test and refine
7. Set up GitHub Pages for hosting
8. Create documentation

## Acceptance Criteria

- RSS feed is generated daily at 12:37 AM AWST
- Feed contains only articles from the past 24 hours
- AFLW articles and other configured filters are excluded
- No duplicate articles appear in the feed
- Feed is accessible via GitHub Pages
- Configuration changes don't require code modifications

This specification provides all necessary details for a developer to implement the AFL.com.au RSS feed generator with configurable filtering capabilities.
