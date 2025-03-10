"""Main entry point for the AFL RSS feed generator."""

import os
import json
from datetime import datetime, timedelta
import pytz
from typing import Dict, List

from scraper import AFLScraper
from feed_generator import AFLFeedGenerator
from utils import load_config, should_filter_article

def load_state(state_file: str = 'previously_scraped.json') -> Dict:
    """
    Load the state from file or create a new one.
    
    Args:
        state_file: Path to the state file.
        
    Returns:
        Dictionary containing the state.
    """
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading state file: {e}")
    
    return {
        'last_run': datetime.utcnow().isoformat(),
        'articles': []
    }

def save_state(state: Dict, state_file: str = 'previously_scraped.json'):
    """
    Save the state to file.
    
    Args:
        state: State dictionary to save.
        state_file: Path where to save the state.
    """
    try:
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Error saving state file: {e}")

def is_article_new(article: Dict[str, str], state: Dict) -> bool:
    """
    Check if an article is new (not previously scraped).
    
    Args:
        article: Article dictionary.
        state: Current state dictionary.
        
    Returns:
        True if the article is new, False otherwise.
    """
    return not any(a['url'] == article['url'] for a in state['articles'])

def is_article_recent(article: Dict[str, str], hours: int = 24) -> bool:
    """
    Check if an article is recent.
    
    Args:
        article: Article dictionary.
        hours: Number of hours to consider recent.
        
    Returns:
        True if the article is recent, False otherwise.
    """
    try:
        pub_date = datetime.fromisoformat(article['pub_date'])
        cutoff = datetime.now(pytz.UTC) - timedelta(hours=hours)
        return pub_date >= cutoff
    except Exception:
        return False

def update_state(state: Dict, articles: List[Dict[str, str]]):
    """
    Update the state with new articles.
    
    Args:
        state: Current state dictionary.
        articles: List of new articles to add.
    """
    state['last_run'] = datetime.utcnow().isoformat()
    
    # Add new articles to state
    for article in articles:
        if is_article_new(article, state):
            state['articles'].append({
                'url': article['url'],
                'pub_date': article['pub_date']
            })
    
    # Keep only recent articles in state
    cutoff = datetime.now(pytz.UTC) - timedelta(days=7)
    state['articles'] = [
        a for a in state['articles']
        if datetime.fromisoformat(a['pub_date']) >= cutoff
    ]

def main():
    """Main function to run the AFL RSS feed generator."""
    try:
        # Load configuration and state
        config = load_config()
        state = load_state()
        
        # Scrape articles
        scraper = AFLScraper(max_pages=5)
        articles = scraper.scrape_articles()
        
        # Filter articles
        filtered_articles = [
            article for article in articles
            if (not should_filter_article(article, config) and
                is_article_new(article, state) and
                is_article_recent(article))
        ]
        
        if not filtered_articles:
            print("No new articles to add to feed.")
            return
        
        # Generate feed
        feed_gen = AFLFeedGenerator()
        feed_gen.add_articles(filtered_articles)
        feed_gen.generate_feed('feed.xml')
        
        # Update state
        update_state(state, filtered_articles)
        save_state(state)
        
        print(f"Successfully added {len(filtered_articles)} new articles to feed.")
        
    except Exception as e:
        print(f"Error running AFL RSS feed generator: {e}")
        raise

if __name__ == '__main__':
    main() 