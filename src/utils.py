"""Utility functions for the AFL RSS feed generator."""

import os
import yaml
from typing import Dict, List, Any, Optional

def load_config(config_path: str = "config.yml") -> Dict[str, Any]:
    """
    Load and parse the YAML configuration file.
    
    Args:
        config_path: Path to the configuration file.
        
    Returns:
        Dict containing the configuration.
        
    Raises:
        FileNotFoundError: If config file doesn't exist and can't create default.
        yaml.YAMLError: If config file is malformed.
    """
    if not os.path.exists(config_path):
        return create_default_config(config_path)
        
    with open(config_path, 'r', encoding='utf-8') as f:
        try:
            config = yaml.safe_load(f)
            return validate_config(config)
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}")
            return create_default_config(config_path)

def create_default_config(config_path: str) -> Dict[str, Any]:
    """
    Create a default configuration file.
    
    Args:
        config_path: Path where to save the default config.
        
    Returns:
        Dict containing the default configuration.
    """
    default_config = {
        'filters': {
            'url_patterns': ['/aflw/'],
            'title_keywords': ['AFLW']
        }
    }
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(default_config, f, default_flow_style=False)
    except Exception as e:
        print(f"Warning: Could not save default config to {config_path}: {e}")
        
    return default_config

def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate the configuration structure and set defaults if needed.
    
    Args:
        config: Configuration dictionary to validate.
        
    Returns:
        Validated configuration dictionary.
    """
    if not isinstance(config, dict):
        return create_default_config("config.yml")
        
    if 'filters' not in config:
        config['filters'] = {}
        
    filters = config['filters']
    if not isinstance(filters, dict):
        config['filters'] = {}
        filters = config['filters']
        
    if 'url_patterns' not in filters:
        filters['url_patterns'] = []
    if 'title_keywords' not in filters:
        filters['title_keywords'] = []
        
    return config

def is_url_filtered(url: str, filter_patterns: List[str]) -> bool:
    """
    Check if a URL matches any of the filter patterns.
    
    Args:
        url: The URL to check.
        filter_patterns: List of patterns to match against.
        
    Returns:
        True if the URL should be filtered out, False otherwise.
    """
    return any(pattern in url for pattern in filter_patterns)

def is_title_filtered(title: str, filter_keywords: List[str]) -> bool:
    """
    Check if a title contains any of the filter keywords.
    
    Args:
        title: The title to check.
        filter_keywords: List of keywords to match against.
        
    Returns:
        True if the title should be filtered out, False otherwise.
    """
    return any(keyword.lower() in title.lower() for keyword in filter_keywords)

def should_filter_article(article: Dict[str, str], config: Dict[str, Any]) -> bool:
    """
    Check if an article should be filtered based on configuration.
    
    Args:
        article: Dictionary containing article data (must have 'url' and 'title' keys).
        config: Configuration dictionary with filter rules.
        
    Returns:
        True if the article should be filtered out, False otherwise.
    """
    filters = config.get('filters', {})
    url_patterns = filters.get('url_patterns', [])
    title_keywords = filters.get('title_keywords', [])
    
    if not article.get('url') or not article.get('title'):
        return True
        
    return (is_url_filtered(article['url'], url_patterns) or 
            is_title_filtered(article['title'], title_keywords)) 