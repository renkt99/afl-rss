"""Tests for RSS feed generation functionality."""

import os
import pytest
from datetime import datetime
import pytz
import xml.etree.ElementTree as ET
from src.feed_generator import AFLFeedGenerator

@pytest.fixture
def feed_generator():
    """Create a feed generator instance for testing."""
    return AFLFeedGenerator()

@pytest.fixture
def sample_article():
    """Create a sample article for testing."""
    return {
        'title': 'Test AFL Article',
        'url': 'https://www.afl.com.au/news/123456/test-article',
        'description': 'This is a test article description.',
        'pub_date': datetime.now(pytz.UTC).isoformat()
    }

def test_feed_metadata(feed_generator):
    """Test feed metadata setup."""
    feed = feed_generator.fg
    
    assert feed.title() == 'AFL.com.au News'
    assert feed.link() == {'href': 'https://www.afl.com.au/news', 'rel': 'alternate'}
    assert feed.description() == 'Latest news from AFL.com.au'
    assert feed.language() == 'en'
    assert feed.author() == {'name': 'AFL.com.au'}

def test_add_article(feed_generator, sample_article, tmp_path):
    """Test adding a single article to the feed."""
    feed_generator.add_article(sample_article)
    
    # Generate feed to test
    output_file = tmp_path / "test_feed.xml"
    feed_generator.generate_feed(str(output_file))
    
    # Parse and verify the feed
    tree = ET.parse(output_file)
    root = tree.getroot()
    
    # Find the item in the feed
    item = root.find('.//item')
    assert item is not None
    
    assert item.find('title').text == sample_article['title']
    assert item.find('link').text == sample_article['url']
    assert item.find('description').text == sample_article['description']
    assert item.find('guid').text == sample_article['url']

def test_add_multiple_articles(feed_generator, sample_article, tmp_path):
    """Test adding multiple articles to the feed."""
    articles = [
        sample_article,
        {
            'title': 'Another Test Article',
            'url': 'https://www.afl.com.au/news/654321/another-article',
            'description': 'Another test description.',
            'pub_date': datetime.now(pytz.UTC).isoformat()
        }
    ]
    
    feed_generator.add_articles(articles)
    
    # Generate feed to test
    output_file = tmp_path / "test_feed.xml"
    feed_generator.generate_feed(str(output_file))
    
    # Parse and verify the feed
    tree = ET.parse(output_file)
    root = tree.getroot()
    
    # Check number of items
    items = root.findall('.//item')
    assert len(items) == len(articles)
    
    # Verify each article
    for item, article in zip(items, articles):
        assert item.find('title').text == article['title']
        assert item.find('link').text == article['url']
        assert item.find('description').text == article['description']

def test_add_article_missing_fields(feed_generator):
    """Test adding an article with missing fields."""
    incomplete_article = {
        'title': 'Test Article',
        # Missing url and description
        'pub_date': datetime.now(pytz.UTC).isoformat()
    }
    
    # Should not raise an exception
    feed_generator.add_article(incomplete_article)

def test_add_article_invalid_date(feed_generator, sample_article):
    """Test adding an article with invalid date."""
    article = sample_article.copy()
    article['pub_date'] = 'invalid-date'
    
    # Should not raise an exception
    feed_generator.add_article(article)

def test_generate_feed_file_error(feed_generator, sample_article):
    """Test handling of file write errors."""
    feed_generator.add_article(sample_article)
    
    with pytest.raises(Exception):
        # Try to write to an invalid location
        feed_generator.generate_feed('/invalid/path/feed.xml')

def test_feed_rss_compliance(feed_generator, sample_article, tmp_path):
    """Test RSS 2.0 compliance of generated feed."""
    feed_generator.add_article(sample_article)
    
    output_file = tmp_path / "test_feed.xml"
    feed_generator.generate_feed(str(output_file))
    
    # Parse and verify RSS 2.0 compliance
    tree = ET.parse(output_file)
    root = tree.getroot()
    
    # Check RSS version
    assert root.tag == 'rss'
    assert root.attrib['version'] == '2.0'
    
    # Check required channel elements
    channel = root.find('channel')
    assert channel is not None
    assert channel.find('title') is not None
    assert channel.find('link') is not None
    assert channel.find('description') is not None
    
    # Check item elements
    item = channel.find('item')
    assert item is not None
    assert item.find('title') is not None
    assert item.find('link') is not None
    assert item.find('description') is not None
    assert item.find('guid') is not None
    assert item.find('pubDate') is not None

def test_feed_with_special_characters(feed_generator, tmp_path):
    """Test handling of special characters in feed content."""
    article = {
        'title': 'Test & Special < > " \' Characters',
        'url': 'https://www.afl.com.au/news/123456/special-chars',
        'description': 'Description with & < > " \' characters',
        'pub_date': datetime.now(pytz.UTC).isoformat()
    }
    
    feed_generator.add_article(article)
    
    output_file = tmp_path / "test_feed.xml"
    feed_generator.generate_feed(str(output_file))
    
    # Verify the file can be parsed
    tree = ET.parse(output_file)
    root = tree.getroot()
    
    # Check that special characters are properly escaped
    item = root.find('.//item')
    assert item is not None
    assert '&' in item.find('title').text
    assert '<' in item.find('description').text

def test_empty_feed_generation(feed_generator, tmp_path):
    """Test generating a feed with no articles."""
    output_file = tmp_path / "test_feed.xml"
    feed_generator.generate_feed(str(output_file))
    
    # Verify the file exists and is valid XML
    tree = ET.parse(output_file)
    root = tree.getroot()
    
    # Should have channel but no items
    channel = root.find('channel')
    assert channel is not None
    items = channel.findall('item')
    assert len(items) == 0 