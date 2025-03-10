"""Tests for main application functionality."""

import os
import json
import pytest
from datetime import datetime, timedelta
import pytz
import xml.etree.ElementTree as ET
from src.main import (
    load_state,
    save_state,
    is_article_new,
    is_article_recent,
    update_state,
    main
)

@pytest.fixture
def sample_state():
    """Create a sample state for testing."""
    return {
        'last_run': datetime.utcnow().isoformat(),
        'articles': [
            {
                'url': 'https://www.afl.com.au/news/123456/old-article',
                'pub_date': (datetime.now(pytz.UTC) - timedelta(days=2)).isoformat()
            },
            {
                'url': 'https://www.afl.com.au/news/654321/recent-article',
                'pub_date': datetime.now(pytz.UTC).isoformat()
            }
        ]
    }

@pytest.fixture
def sample_article():
    """Create a sample article for testing."""
    return {
        'title': 'Test AFL Article',
        'url': 'https://www.afl.com.au/news/999999/test-article',
        'description': 'This is a test article description.',
        'pub_date': datetime.now(pytz.UTC).isoformat()
    }

def test_load_state_existing(tmp_path, sample_state):
    """Test loading an existing state file."""
    state_file = tmp_path / "test_state.json"
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(sample_state, f)
    
    loaded_state = load_state(state_file)
    assert loaded_state == sample_state

def test_load_state_missing():
    """Test loading a non-existent state file."""
    state = load_state('nonexistent.json')
    assert isinstance(state, dict)
    assert 'last_run' in state
    assert 'articles' in state
    assert len(state['articles']) == 0

def test_load_state_invalid_json(tmp_path):
    """Test loading an invalid state file."""
    state_file = tmp_path / "invalid_state.json"
    with open(state_file, 'w', encoding='utf-8') as f:
        f.write("invalid json content")
    
    state = load_state(state_file)
    assert isinstance(state, dict)
    assert 'last_run' in state
    assert 'articles' in state

def test_save_state(tmp_path, sample_state):
    """Test saving state to file."""
    state_file = tmp_path / "test_state.json"
    save_state(sample_state, state_file)
    
    assert os.path.exists(state_file)
    with open(state_file, 'r', encoding='utf-8') as f:
        loaded_state = json.load(f)
    assert loaded_state == sample_state

def test_save_state_error():
    """Test handling of state save errors."""
    # Try to save to an invalid location
    save_state({}, '/invalid/path/state.json')
    # Should not raise an exception

def test_is_article_new(sample_state, sample_article):
    """Test checking if an article is new."""
    assert is_article_new(sample_article, sample_state)
    
    # Test with existing article
    existing_article = {
        'url': sample_state['articles'][0]['url'],
        'pub_date': datetime.now(pytz.UTC).isoformat()
    }
    assert not is_article_new(existing_article, sample_state)

def test_is_article_recent():
    """Test checking if an article is recent."""
    now = datetime.now(pytz.UTC)
    
    # Recent article
    recent_article = {
        'pub_date': now.isoformat()
    }
    assert is_article_recent(recent_article)
    
    # Old article
    old_article = {
        'pub_date': (now - timedelta(hours=25)).isoformat()
    }
    assert not is_article_recent(old_article)
    
    # Invalid date
    invalid_article = {
        'pub_date': 'invalid-date'
    }
    assert not is_article_recent(invalid_article)

def test_update_state(sample_state, sample_article):
    """Test updating state with new articles."""
    original_count = len(sample_state['articles'])
    update_state(sample_state, [sample_article])
    
    assert len(sample_state['articles']) == original_count + 1
    assert any(a['url'] == sample_article['url'] for a in sample_state['articles'])

def test_update_state_cleanup(sample_state):
    """Test cleanup of old articles during state update."""
    # Add some very old articles
    old_articles = [
        {
            'url': f'https://www.afl.com.au/news/{i}/old-article',
            'pub_date': (datetime.now(pytz.UTC) - timedelta(days=10)).isoformat()
        }
        for i in range(5)
    ]
    
    update_state(sample_state, old_articles)
    
    # Check that old articles were removed
    assert all(
        datetime.fromisoformat(a['pub_date']) >= datetime.now(pytz.UTC) - timedelta(days=7)
        for a in sample_state['articles']
    )

def test_main_integration(tmp_path, requests_mock):
    """Test complete main function flow."""
    # Set up mock responses
    html_content = """
    <html>
        <article>
            <h2>Test AFL Article</h2>
            <a href="/news/123456/test-article">Read More</a>
            <p>Test description</p>
            <time datetime="2024-03-09T10:00:00+11:00">March 9, 2024</time>
        </article>
    </html>
    """
    requests_mock.get('https://www.afl.com.au/news', text=html_content)
    
    # Set up test files
    os.chdir(tmp_path)
    
    # Create config file
    with open('config.yml', 'w', encoding='utf-8') as f:
        f.write("""
filters:
  url_patterns:
    - "/aflw/"
  title_keywords:
    - "AFLW"
        """)
    
    # Run main function
    main()
    
    # Verify feed was generated
    assert os.path.exists('feed.xml')
    
    # Verify state was saved
    assert os.path.exists('previously_scraped.json')
    
    # Verify feed content
    tree = ET.parse('feed.xml')
    root = tree.getroot()
    
    # Should have at least one item
    items = root.findall('.//item')
    assert len(items) > 0

def test_main_no_new_articles(tmp_path, requests_mock):
    """Test main function when no new articles are found."""
    # Set up mock response with no articles
    html_content = "<html><body></body></html>"
    requests_mock.get('https://www.afl.com.au/news', text=html_content)
    
    # Set up test files
    os.chdir(tmp_path)
    
    # Create config file
    with open('config.yml', 'w', encoding='utf-8') as f:
        f.write("""
filters:
  url_patterns: []
  title_keywords: []
        """)
    
    # Run main function
    main()
    
    # Feed should not be generated
    assert not os.path.exists('feed.xml')

def test_main_error_handling(tmp_path, requests_mock):
    """Test main function error handling."""
    # Set up mock to simulate network error
    requests_mock.get('https://www.afl.com.au/news', exc=Exception('Network error'))
    
    # Set up test files
    os.chdir(tmp_path)
    
    # Create config file
    with open('config.yml', 'w', encoding='utf-8') as f:
        f.write("""
filters:
  url_patterns: []
  title_keywords: []
        """)
    
    # Run main function (should raise exception)
    with pytest.raises(Exception):
        main() 