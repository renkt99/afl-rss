"""Tests for web scraping functionality."""

import pytest
import requests
import requests_mock
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from src.scraper import AFLScraper

@pytest.fixture
def sample_article_html():
    """Create a sample article HTML fixture."""
    return """
    <article class="article-item">
        <h2 class="article-title">Test AFL Article</h2>
        <a href="/news/123456/test-article">Read More</a>
        <p class="article-description">This is a test article description.</p>
        <time datetime="2024-03-09T10:00:00+11:00">March 9, 2024</time>
    </article>
    """

@pytest.fixture
def sample_page_html(sample_article_html):
    """Create a sample page HTML fixture with multiple articles."""
    return f"""
    <html>
    <body>
        <div class="news-list">
            {sample_article_html}
            <article class="article-item">
                <h2 class="article-title">Another AFL Article</h2>
                <a href="/news/654321/another-article">Read More</a>
                <p class="article-description">This is another test article.</p>
                <time datetime="2024-03-09T09:00:00+11:00">March 9, 2024</time>
            </article>
        </div>
        <div class="pagination">
            <a href="/news/page/2" rel="next">Next</a>
        </div>
    </body>
    </html>
    """

@pytest.fixture
def scraper():
    """Create a scraper instance for testing."""
    return AFLScraper(max_pages=2)

def test_fetch_page_success(scraper, requests_mock, sample_page_html):
    """Test successful page fetching."""
    requests_mock.get(AFLScraper.BASE_URL, text=sample_page_html)
    content = scraper.fetch_page(AFLScraper.BASE_URL)
    assert content == sample_page_html
    assert requests_mock.call_count == 1

def test_fetch_page_404(scraper, requests_mock):
    """Test handling of HTTP 404 error."""
    requests_mock.get(AFLScraper.BASE_URL, status_code=404)
    content = scraper.fetch_page(AFLScraper.BASE_URL)
    assert content is None

def test_fetch_page_connection_error(scraper, requests_mock):
    """Test handling of connection error."""
    requests_mock.get(AFLScraper.BASE_URL, exc=requests.ConnectionError)
    content = scraper.fetch_page(AFLScraper.BASE_URL)
    assert content is None

def test_fetch_page_timeout(scraper, requests_mock):
    """Test handling of timeout error."""
    requests_mock.get(AFLScraper.BASE_URL, exc=requests.Timeout)
    content = scraper.fetch_page(AFLScraper.BASE_URL)
    assert content is None

def test_parse_article_complete(scraper, sample_article_html):
    """Test parsing a complete article."""
    soup = BeautifulSoup(sample_article_html, 'html.parser')
    article = scraper.parse_article(soup)
    
    assert article is not None
    assert article['title'] == 'Test AFL Article'
    assert article['url'] == 'https://www.afl.com.au/news/123456/test-article'
    assert article['description'] == 'This is a test article description.'
    assert datetime.fromisoformat(article['pub_date']).tzinfo is not None

def test_parse_article_missing_fields(scraper):
    """Test parsing an article with missing fields."""
    html = """
    <article>
        <h2>Test Title</h2>
        <!-- Missing link and other fields -->
    </article>
    """
    soup = BeautifulSoup(html, 'html.parser')
    article = scraper.parse_article(soup)
    assert article is None

def test_parse_article_empty(scraper):
    """Test parsing an empty article element."""
    soup = BeautifulSoup('<article></article>', 'html.parser')
    article = scraper.parse_article(soup)
    assert article is None

def test_parse_page(scraper, sample_page_html):
    """Test parsing a complete page."""
    articles = scraper.parse_page(sample_page_html)
    assert len(articles) == 2
    assert all(isinstance(a, dict) for a in articles)
    assert all(set(a.keys()) == {'title', 'url', 'description', 'pub_date'} for a in articles)

def test_parse_page_no_articles(scraper):
    """Test parsing a page with no articles."""
    html = "<html><body><div class='news-list'></div></body></html>"
    articles = scraper.parse_page(html)
    assert len(articles) == 0

def test_parse_page_invalid_html(scraper):
    """Test parsing invalid HTML."""
    articles = scraper.parse_page("invalid html content")
    assert len(articles) == 0

def test_extract_next_page_url(scraper, sample_page_html):
    """Test extracting next page URL."""
    next_url = scraper.extract_next_page_url(sample_page_html)
    assert next_url == "https://www.afl.com.au/news/page/2"

def test_extract_next_page_url_none(scraper):
    """Test extracting next page URL when none exists."""
    html = "<html><body><div class='pagination'></div></body></html>"
    next_url = scraper.extract_next_page_url(html)
    assert next_url is None

def test_scrape_articles_single_page(scraper, requests_mock, sample_page_html):
    """Test scraping articles from a single page."""
    requests_mock.get(AFLScraper.BASE_URL, text=sample_page_html)
    articles = scraper.scrape_articles()
    assert len(articles) == 2
    assert requests_mock.call_count == 1

def test_scrape_articles_multiple_pages(scraper, requests_mock, sample_page_html):
    """Test scraping articles from multiple pages."""
    # First page
    requests_mock.get(AFLScraper.BASE_URL, text=sample_page_html)
    # Second page
    requests_mock.get('https://www.afl.com.au/news/page/2', text=sample_page_html)
    
    articles = scraper.scrape_articles()
    assert len(articles) == 4  # 2 articles per page * 2 pages
    assert requests_mock.call_count == 2

def test_scrape_articles_max_pages(scraper, requests_mock, sample_page_html):
    """Test respecting max_pages limit."""
    # Configure mock to always return a page with a next link
    requests_mock.get(requests_mock.ANY, text=sample_page_html)
    
    articles = scraper.scrape_articles()
    assert len(articles) == 4  # 2 articles per page * 2 pages (max_pages=2)
    assert requests_mock.call_count == 2  # Should only fetch 2 pages

def test_scrape_articles_error_handling(scraper, requests_mock):
    """Test error handling during scraping."""
    # First page fails
    requests_mock.get(AFLScraper.BASE_URL, status_code=500)
    
    articles = scraper.scrape_articles()
    assert len(articles) == 0
    assert requests_mock.call_count == 1 