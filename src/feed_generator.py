"""RSS feed generator for AFL.com.au news articles."""

from feedgen.feed import FeedGenerator
from typing import Dict, List
from datetime import datetime
import pytz

class AFLFeedGenerator:
    """Generator for AFL.com.au RSS feed."""
    
    def __init__(self):
        """Initialize the feed generator with basic feed metadata."""
        self.fg = FeedGenerator()
        self.setup_feed_metadata()
    
    def setup_feed_metadata(self):
        """Set up the basic feed metadata."""
        self.fg.title('AFL.com.au News')
        self.fg.link(href='https://www.afl.com.au/news', rel='alternate')
        self.fg.description('Latest news from AFL.com.au')
        self.fg.language('en')
        self.fg.author({'name': 'AFL.com.au'})
        self.fg.generator('AFL RSS Feed Generator')
    
    def add_article(self, article: Dict[str, str]):
        """
        Add an article to the feed.
        
        Args:
            article: Dictionary containing article data.
                    Must have 'title', 'url', 'description', and 'pub_date' keys.
        """
        try:
            entry = self.fg.add_entry()
            entry.title(article['title'])
            entry.link(href=article['url'])
            entry.description(article['description'])
            
            # Parse the ISO format date string
            pub_date = datetime.fromisoformat(article['pub_date'])
            entry.published(pub_date)
            entry.updated(pub_date)
            
            # Use URL as unique identifier
            entry.id(article['url'])
            
        except Exception as e:
            print(f"Error adding article to feed: {e}")
    
    def add_articles(self, articles: List[Dict[str, str]]):
        """
        Add multiple articles to the feed.
        
        Args:
            articles: List of article dictionaries.
        """
        for article in articles:
            self.add_article(article)
    
    def generate_feed(self, output_file: str = 'feed.xml'):
        """
        Generate the RSS feed file.
        
        Args:
            output_file: Path where to save the feed XML file.
        """
        try:
            self.fg.rss_file(output_file, pretty=True)
            print(f"Feed generated successfully: {output_file}")
        except Exception as e:
            print(f"Error generating feed file: {e}")
            raise 