# AFL.com.au RSS Feed Generator: Implementation Plan & Prompts

This document provides a comprehensive blueprint for building an AFL.com.au RSS feed generator based on the provided specification. It breaks down the implementation into small, iterative chunks that build on each other, ensuring incremental progress with robust testing at every stage.

## Project Overview

A scheduled web scraper that generates a standard RSS feed for AFL.com.au news articles, with configurable content filtering capabilities. The system will:

- Scrape the AFL.com.au news page daily
- Filter content based on configurable criteria
- Generate a standard RSS 2.0 feed
- Track previously scraped articles to prevent duplicates
- Run automatically via GitHub Actions
- Deliver the feed via GitHub Pages

## Implementation Blueprint

### High-Level Structure

1. **Project Setup**: Create repository structure, set up environment, and initialize files
2. **Configuration Management**: Implement config parsing and filtering logic
3. **Web Scraping**: Develop scraper for AFL.com.au news articles
4. **State Management**: Create system to track previously scraped articles
5. **RSS Feed Generation**: Build the RSS feed generator
6. **Integration**: Connect all components into a cohesive application
7. **GitHub Actions & Pages**: Set up automated workflow and hosting
8. **Documentation**: Create comprehensive documentation

### Implementation Prompts

These prompts are designed to be sent to a code-generation LLM to implement each step in a test-driven manner. Each prompt builds on the previous one, ensuring incremental progress with strong testing.

#### Prompt 1: Basic Project Setup

```
Let's create a Python project that will scrape AFL.com.au and generate an RSS feed. We'll build this incrementally with a test-driven approach.

For this first step, please:

1. Create the basic directory structure as specified below:
   - .github/workflows/ (empty directory for now)
   - src/ (will contain our Python modules)
   - tests/ (for our test files)

2. Create the following empty placeholder files:
   - src/scraper.py (will handle web scraping)
   - src/feed_generator.py (will generate the RSS feed)
   - src/utils.py (for helper functions)
   - src/main.py (entry point)
   - config.yml (empty configuration file)
   - requirements.txt (with initial dependencies)

3. In requirements.txt, include the following dependencies:
   - requests
   - beautifulsoup4
   - feedgen
   - PyYAML
   - pytest (for testing)

4. Create a basic README.md with project title and a brief description.

Please provide the file structure and content for each file, keeping them minimal but functional placeholders that we'll expand in later steps.
```

#### Prompt 2: Configuration System - Basic Structure

```
Now let's implement the configuration system for our AFL RSS feed generator. The configuration will control what content is filtered from the feed.

1. Create a basic config.yml file with the following structure:
   - filters section with url_patterns and title_keywords lists
   - Include the default filter to exclude AFLW articles ("/aflw/")

2. In src/utils.py, implement:
   - A function to load and parse the YAML configuration file
   - Basic error handling for missing or malformed config files
   - A function to create a default configuration if none exists

3. Create tests/test_utils.py with:
   - Unit tests for the configuration loading function
   - Tests for handling missing config files
   - Tests for validating config structure

Remember to use a test-driven approach: write tests first, then implement the functions to pass the tests. Ensure that if the config file is missing, a default configuration is used that excludes AFLW articles.
```

#### Prompt 3: Configuration System - Filtering Logic

```
Let's continue building our AFL RSS feed generator by implementing the filtering logic based on the configuration.

1. In src/utils.py, implement the following functions:
   - is_url_filtered(url, filter_patterns): Returns True if the URL matches any filter pattern
   - is_title_filtered(title, filter_keywords): Returns True if the title contains any filtered keywords
   - should_filter_article(article, config): Combined function that checks both URL and title against filters

2. Enhance tests/test_utils.py with:
   - Unit tests for is_url_filtered with various URLs and patterns
   - Unit tests for is_title_filtered with various titles and keywords
   - Unit tests for should_filter_article with different combinations

3. Update the default configuration generation to include empty lists for both filter types if not specified.

Remember to focus on clean, well-documented code with appropriate error handling. Each function should have docstrings explaining its purpose, parameters, and return values.
```

#### Prompt 4: Basic Web Scraper - HTTP Requests

```
Now let's start implementing the web scraper component that will fetch content from AFL.com.au.

1. In src/scraper.py, implement:
   - A function fetch_afl_news_page(url) that makes an HTTP request to the AFL news page
   - Proper error handling for connection issues, timeouts, and HTTP errors
   - Return the HTML content when successful

2. Create tests/test_scraper.py with:
   - Unit tests for fetch_afl_news_page using requests-mock to simulate responses
   - Tests for various error conditions (connection error, timeout, HTTP 404, etc.)
   - Tests for successful page retrieval

3. Update requirements.txt to include:
   - requests-mock (for testing the HTTP requests)

For the implementation, use the requests library with appropriate timeouts and user-agent headers. Make sure the function is well-documented with docstrings and handles all potential error cases gracefully.
```

#### Prompt 5: Basic Web Scraper - HTML Parsing

```
Let's continue developing our web scraper by implementing the HTML parsing component to extract article information.

1. In src/scraper.py, implement:
   - A function parse_afl_news_page(html_content) that uses BeautifulSoup to extract:
     - Article titles
     - Article URLs
     - Returns a list of dictionaries with 'title' and 'url' keys

2. Enhance tests/test_scraper.py with:
   - Create a sample HTML fixture that mimics the AFL news page structure
   - Unit tests for parse_afl_news_page using the fixture
   - Tests for handling empty or invalid HTML
   - Tests for correctly extracting article information

3. Create a simple Article class or named tuple for storing article information consistently.

Use BeautifulSoup with the 'html.parser' parser for parsing. Focus on making the parsing function robust against potential HTML structure changes by using appropriate selectors and error handling.
```

#### Prompt 6: Advanced Web Scraper - Article Details

```
Let's enhance our web scraper to extract more detailed article information from the AFL news page.

1. In src/scraper.py, extend the parse_afl_news_page function to extract:
   - Article descriptions/summaries
   - Publication dates
   - Update the article data structure to include these new fields

2. Implement a function parse_date(date_string) that:
   - Converts AFL's date format to a standard datetime object
   - Handles potential variations in date formats
   - Returns an ISO 8601 formatted string

3. Update tests/test_scraper.py with:
   - Enhanced HTML fixtures that include descriptions and dates
   - Tests for parsing descriptions and dates
   - Tests for date format conversion
   - Tests for handling missing or malformed date information

Ensure that the parser is robust against potential changes in the page structure and handles cases where some information might be missing.
```

#### Prompt 7: Advanced Web Scraper - Pagination

```
Let's further enhance our web scraper to handle pagination, ensuring we can get all recent articles from the AFL news page.

1. In src/scraper.py, implement:
   - A function extract_pagination_links(html_content) that identifies next page links
   - Modify the scraping function to handle pagination by:
     - Detecting if there are more pages
     - Fetching and parsing subsequent pages
     - Combining articles from all pages

2. Create a new function scrape_afl_news(base_url, max_pages=5) that:
   - Coordinates the entire scraping process
   - Limits the number of pages to prevent infinite loops
   - Returns a complete list of articles from all scraped pages

3. Update tests/test_scraper.py with:
   - Tests for pagination link extraction
   - Tests for the combined scraping function with multiple pages
   - Tests for handling the max_pages limit

Make sure the implementation gracefully handles cases where pagination is not present or structured differently than expected.
```

#### Prompt 8: State Management - Basic Structure

```
Now let's implement the state management system to keep track of previously scraped articles.

1. Create a new file src/state_manager.py with:
   - A function load_state(file_path) to load the previously_scraped.json file
   - A function initialize_state() to create a new state structure if none exists
   - A State class or structure to manage the state information

2. Implement the state structure as specified in the requirements:
   - last_run timestamp (ISO 8601 format)
   - articles list with url and published fields

3. Create tests/test_state_manager.py with:
   - Tests for loading existing state files
   - Tests for initializing new state when file doesn't exist
   - Tests for validating state structure

4. Create a sample previously_scraped.json file for testing purposes.

Ensure proper error handling for file operations and JSON parsing. The state management should be resilient to file corruption or unexpected formats.
```

#### Prompt 9: State Management - Article Tracking

```
Let's extend our state management system to handle tracking of articles and prevent duplicates.

1. In src/state_manager.py, implement:
   - A function is_article_scraped(article, state) to check if an article is already in the state
   - A function add_article_to_state(article, state) to add a new article to the state
   - A function save_state(state, file_path) to write the updated state to file

2. Implement a function get_new_articles(articles, state) that:
   - Filters out articles already in the state
   - Returns only new articles to be processed

3. Update tests/test_state_manager.py with:
   - Tests for checking if articles are already scraped
   - Tests for adding new articles to state
   - Tests for saving state to file
   - Tests for filtering to get only new articles

4. Implement proper date handling to ensure consistency between scraper dates and state dates.

Make sure the implementation handles edge cases like duplicate URLs with different dates, and uses proper serialization for datetime objects.
```

#### Prompt 10: Content Filtering - Time-Based Selection

```
Let's implement the time-based filtering to include only recent articles in our RSS feed.

1. In src/utils.py, implement:
   - A function is_article_recent(article, hours=24) that:
     - Checks if the article's publication date is within the specified number of hours
     - Returns True for recent articles, False otherwise

2. Create a function filter_recent_articles(articles, hours=24) that:
   - Takes a list of articles and filters out non-recent ones
   - Returns only articles published within the specified timeframe

3. Update tests/test_utils.py with:
   - Tests for is_article_recent with various publication dates
   - Tests for filter_recent_articles with mixed article dates
   - Tests for handling edge cases like missing dates

4. Ensure proper datetime handling and timezone awareness.

The implementation should correctly parse the article publication dates, compare them to the current time, and handle timezone differences if present in the data.
```

#### Prompt 11: Feed Generator - Basic Structure

```
Now let's implement the RSS feed generator component.

1. In src/feed_generator.py, implement:
   - A function initialize_feed() that creates a new FeedGenerator instance
   - Set up the basic feed metadata:
     - Title: "afl.com.au"
     - Link to AFL website
     - Description: "Latest news from AFL.com.au"
     - Language: "en"

2. Implement a function add_article_to_feed(feed, article) that:
   - Adds an article as an item to the feed
   - Sets all required item fields (title, link, description, etc.)
   - Formats the publication date according to RFC 822 standard

3. Create tests/test_feed_generator.py with:
   - Tests for feed initialization with correct metadata
   - Tests for adding articles to the feed
   - Tests for date formatting

4. Update requirements.txt to include feedgen if not already included.

Ensure the feed generator produces standard-compliant RSS 2.0 format. Use proper date formatting and handle potential missing fields in articles.
```

#### Prompt 12: Feed Generator - Complete

```
Let's complete the RSS feed generator implementation with advanced features.

1. In src/feed_generator.py, implement:
   - A function generate_feed(articles) that:
     - Initializes a new feed
     - Adds all articles to the feed
     - Returns the complete feed object

2. Implement a function save_feed(feed, file_path) that:
   - Saves the feed to an XML file at the specified path
   - Handles file writing errors

3. Update tests/test_feed_generator.py with:
   - Tests for the complete feed generation with multiple articles
   - Tests for feed saving
   - Tests for handling edge cases like empty article lists

4. Ensure the feed items include all required fields:
   - Title
   - Link
   - Description
   - Publication date (properly formatted)
   - GUID (using article URL)

Make sure the implementation follows RSS 2.0 standards and produces valid XML. The feed should be usable by standard RSS readers.
```

#### Prompt 13: Main Application - Basic Structure

```
Now let's start integrating all the components into the main application flow.

1. In src/main.py, implement:
   - A function setup_logging() to configure logging
   - A function load_config() to load the configuration
   - A main() function that will coordinate the entire process

2. Begin implementing the main execution flow:
   - Load configuration
   - Initialize logging
   - Basic error handling structure

3. Create tests/test_main.py with:
   - Tests for the setup_logging function
   - Tests for the load_config function
   - Basic tests for the main function structure

4. Implement a simple command-line interface if needed.

Focus on setting up the foundation for the complete application flow. Make sure logging is properly configured to capture information about the execution process.
```

#### Prompt 14: Main Application - Integration

```
Let's continue integrating the components into the main application flow.

1. In src/main.py, extend the main() function to:
   - Load the current state
   - Scrape the AFL news page
   - Filter articles based on configuration
   - Filter recent articles
   - Compare with state to find new articles
   - Update the state with new articles

2. Implement proper error handling for each step:
   - Log errors but continue execution when possible
   - Fail gracefully when critical errors occur

3. Update tests/test_main.py with:
   - Integration tests for the main flow
   - Tests for handling various error conditions
   - Tests for proper interaction between components

4. Ensure that the main function follows a logical flow and handles errors appropriately.

The focus here is on integrating the scraping, filtering, and state management components. Make sure the application behaves correctly when components fail or return unexpected results.
```

#### Prompt 15: Main Application - Complete

```
Let's complete the main application by integrating the feed generation and final steps.

1. In src/main.py, extend the main() function to:
   - Generate the RSS feed from filtered articles
   - Save the feed to file
   - Save the updated state
   - Log execution summary

2. Implement a function run() that:
   - Calls main() with appropriate error handling
   - Returns exit codes based on execution success/failure
   - Can be used as an entry point for both direct execution and GitHub Actions

3. Update tests/test_main.py with:
   - Complete integration tests for the entire flow
   - Tests for the run function
   - Tests for handling end-to-end scenarios

4. Add if __name__ == "__main__": block to allow direct script execution.

Ensure the application now handles the complete flow from configuration loading to feed generation and state saving. All components should be properly integrated with appropriate error handling.
```

#### Prompt 16: GitHub Actions Workflow

```
Now let's set up the GitHub Actions workflow to automate the RSS feed generation.

1. Create .github/workflows/generate_rss.yml with:
   - The workflow configuration as specified in the requirements
   - Schedule to run daily at 16:37 UTC (12:37 AM AWST)
   - Manual trigger option (workflow_dispatch)
   - Steps to checkout code, set up Python, install dependencies, and run the script
   - Git configuration to commit and push changes

2. Update the README.md with:
   - Information about the GitHub Actions workflow
   - How to trigger the workflow manually
   - Expected behavior of the automated process

3. Ensure the workflow will properly commit and push:
   - feed.xml
   - previously_scraped.json

The workflow should be configured exactly as specified in the requirements document. Make sure it handles potential errors in the commit process (e.g., no changes to commit).
```

#### Prompt 17: GitHub Pages Setup

```
Let's complete the project by setting up GitHub Pages for feed delivery and finalizing documentation.

1. Update the README.md with:
   - Instructions for enabling GitHub Pages in repository settings
   - Information about the feed URL structure
   - Complete setup and usage documentation
   - Configuration options and examples

2. Add information about:
   - How to subscribe to the feed in various RSS readers
   - How to customize the filters in config.yml
   - How to manually trigger the workflow
   - Troubleshooting tips

3. Create a sample HTML page that can be hosted on GitHub Pages to:
   - Provide information about the feed
   - Include a direct link to the feed.xml

4. Update any remaining documentation with integration details.

The focus here is on ensuring that users can easily set up, configure, and use the RSS feed generator. The documentation should be comprehensive but clear and usable.
```

#### Prompt 18: Final Integration and Testing

```
Let's do a final integration and testing pass to ensure everything works together perfectly.

1. Review all components for integration issues:
   - Check for consistent error handling across modules
   - Ensure all components use the same data structures
   - Verify logging is consistent throughout the application

2. Enhance tests with:
   - End-to-end integration tests for the complete flow
   - Tests for edge cases and error conditions
   - Performance tests for large numbers of articles

3. Create a script for local testing that:
   - Simulates the GitHub Actions environment
   - Tests the full execution without committing changes

4. Update any documentation based on the testing results.

The goal is to ensure that all components work together seamlessly and that the application is robust against various failure scenarios. Pay particular attention to edge cases and error conditions.
```

## Implementation Notes

### Development Approach

1. **Test-Driven Development**
   - Each step follows a test-driven approach
   - Tests are written before or alongside implementation
   - Tests cover both success paths and error handling

2. **Incremental Progress**
   - Each step builds on the previous one
   - Functionality is added in small, manageable chunks
   - Each step adds a specific piece of functionality

3. **Robust Error Handling**
   - All components include comprehensive error handling
   - The application can recover from non-critical errors
   - Critical errors are logged appropriately

4. **Component Integration**
   - Components are integrated gradually
   - Integration is tested at each step
   - Data structures are consistent across components

5. **Documentation**
   - Documentation is built alongside the code
   - README.md is updated throughout development
   - User instructions are clear and comprehensive

### Technology Stack

- **Programming Language:** Python 3.x
- **Key Libraries:**
  - BeautifulSoup4 for HTML parsing
  - feedgen for RSS generation
  - requests for HTTP requests
  - PyYAML for configuration management
- **Infrastructure:**
  - GitHub Actions for scheduled execution
  - GitHub Pages for feed hosting

### File Structure

```
/
├── .github/
│   └── workflows/
│       └── generate_rss.yml    # GitHub Actions workflow
├── src/
│   ├── scraper.py              # Web scraping logic
│   ├── feed_generator.py       # RSS feed generation
│   ├── state_manager.py        # State management
│   ├── utils.py                # Helper functions
│   └── main.py                 # Entry point
├── tests/
│   ├── test_scraper.py         # Scraper tests
│   ├── test_feed_generator.py  # Feed generator tests
│   ├── test_state_manager.py   # State management tests
│   ├── test_utils.py           # Utility tests
│   └── test_main.py            # Main application tests
├── config.yml                  # Configuration file
├── previously_scraped.json     # State file
├── feed.xml                    # Generated RSS feed
├── README.md                   # Documentation
└── requirements.txt            # Dependencies
```

This implementation plan provides a step-by-step approach to building the AFL.com.au RSS feed generator, ensuring quality, testability, and maintainability throughout the development process.
