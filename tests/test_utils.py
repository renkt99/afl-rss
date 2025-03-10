"""Tests for utility functions."""

import os
import pytest
import yaml
from src.utils import (
    load_config,
    create_default_config,
    validate_config,
    is_url_filtered,
    is_title_filtered,
    should_filter_article
)

@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary config file for testing."""
    config_path = tmp_path / "config.yml"
    config = {
        'filters': {
            'url_patterns': ['/aflw/', '/test/'],
            'title_keywords': ['AFLW', 'Test']
        }
    }
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(config, f)
    return config_path

def test_load_valid_config(temp_config_file):
    """Test loading a valid configuration file."""
    config = load_config(temp_config_file)
    assert isinstance(config, dict)
    assert 'filters' in config
    assert 'url_patterns' in config['filters']
    assert 'title_keywords' in config['filters']
    assert '/aflw/' in config['filters']['url_patterns']
    assert 'AFLW' in config['filters']['title_keywords']

def test_load_missing_config():
    """Test loading a non-existent configuration file."""
    config = load_config('nonexistent.yml')
    assert isinstance(config, dict)
    assert 'filters' in config
    assert '/aflw/' in config['filters']['url_patterns']
    assert 'AFLW' in config['filters']['title_keywords']

def test_load_invalid_yaml(tmp_path):
    """Test loading an invalid YAML file."""
    config_path = tmp_path / "invalid.yml"
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write("invalid: yaml: content:")
    
    config = load_config(config_path)
    assert isinstance(config, dict)
    assert 'filters' in config

def test_create_default_config(tmp_path):
    """Test creating a default configuration."""
    config_path = tmp_path / "config.yml"
    config = create_default_config(str(config_path))
    
    assert isinstance(config, dict)
    assert 'filters' in config
    assert '/aflw/' in config['filters']['url_patterns']
    assert 'AFLW' in config['filters']['title_keywords']
    assert os.path.exists(config_path)

def test_validate_config_empty():
    """Test validating an empty configuration."""
    config = validate_config({})
    assert isinstance(config, dict)
    assert 'filters' in config
    assert 'url_patterns' in config['filters']
    assert 'title_keywords' in config['filters']

def test_validate_config_invalid_type():
    """Test validating a configuration with invalid type."""
    config = validate_config([])  # List instead of dict
    assert isinstance(config, dict)
    assert 'filters' in config

def test_validate_config_missing_filters():
    """Test validating a configuration with missing filters."""
    config = validate_config({'other': 'value'})
    assert 'filters' in config
    assert 'url_patterns' in config['filters']
    assert 'title_keywords' in config['filters']

def test_url_filtering():
    """Test URL filtering functionality."""
    patterns = ['/aflw/', '/test/']
    
    assert is_url_filtered('/aflw/news', patterns)
    assert is_url_filtered('/test/article', patterns)
    assert not is_url_filtered('/news/article', patterns)
    assert not is_url_filtered('', patterns)
    assert not is_url_filtered('/news/aflw', patterns)  # Should only match exact pattern

def test_title_filtering():
    """Test title filtering functionality."""
    keywords = ['AFLW', 'Test']
    
    assert is_title_filtered('AFLW Match Report', keywords)
    assert is_title_filtered('Test Article', keywords)
    assert is_title_filtered('Match Report AFLW', keywords)
    assert is_title_filtered('aflw match', keywords)  # Case insensitive
    assert not is_title_filtered('AFL Match Report', keywords)
    assert not is_title_filtered('', keywords)

def test_article_filtering():
    """Test complete article filtering."""
    config = {
        'filters': {
            'url_patterns': ['/aflw/'],
            'title_keywords': ['AFLW']
        }
    }
    
    # Should be filtered (AFLW in URL)
    article1 = {
        'url': '/aflw/news/123',
        'title': 'Match Report'
    }
    assert should_filter_article(article1, config)
    
    # Should be filtered (AFLW in title)
    article2 = {
        'url': '/news/123',
        'title': 'AFLW Match Report'
    }
    assert should_filter_article(article2, config)
    
    # Should not be filtered
    article3 = {
        'url': '/news/123',
        'title': 'AFL Match Report'
    }
    assert not should_filter_article(article3, config)
    
    # Should be filtered (missing fields)
    article4 = {
        'url': '/news/123'
    }
    assert should_filter_article(article4, config)
    
    # Should be filtered (empty fields)
    article5 = {
        'url': '',
        'title': ''
    }
    assert should_filter_article(article5, config)

def test_config_with_utf8_chars(tmp_path):
    """Test loading configuration with UTF-8 special characters."""
    config_path = tmp_path / "config.yml"
    config = {
        'filters': {
            'url_patterns': ['/café/', '/über/'],
            'title_keywords': ['café', 'über']
        }
    }
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(config, f)
    
    loaded_config = load_config(config_path)
    assert 'café' in loaded_config['filters']['title_keywords']
    assert 'über' in loaded_config['filters']['url_patterns'] 