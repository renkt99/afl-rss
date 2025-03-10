"""Web scraper for AFL.com.au news articles."""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from datetime import datetime
import pytz

class AFLScraper:
    """Scraper for AFL.com.au news articles."""
    
    BASE_URL = "https://www.afl.com.au/news"
    USER_AGENT = "AFL RSS Feed Generator/1.0"
    TIMEOUT = 30  # seconds
    
    def __init__(self, max_pages: int = 5):
        """
        Initialize the scraper.
        
        Args:
            max_pages: Maximum number of pages to scrape.
        """
        self.max_pages = max_pages
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.USER_AGENT})
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a page from AFL.com.au.
        
        Args:
            url: URL to fetch.
            
        Returns:
            HTML content if successful, None otherwise.
        """
        try:
            response = self.session.get(url, timeout=self.TIMEOUT)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def parse_article(self, article_element: BeautifulSoup) -> Optional[Dict[str, str]]:
        """
        Parse an article element from the news page.
        
        Args:
            article_element: BeautifulSoup element containing article data.
            
        Returns:
            Dictionary with article data if successful, None otherwise.
        """
        try:
            # Note: These selectors will need to be updated based on actual AFL.com.au HTML structure
            title_elem = article_element.find('h2') or article_element.find('h3')
            link_elem = article_element.find('a')
            desc_elem = article_element.find('p')
            date_elem = article_element.find('time')
            
            if not (title_elem and link_elem):
                return None
                
            title = title_elem.get_text().strip()
            url = link_elem.get('href', '')
            if not url.startswith('http'):
                url = f"https://www.afl.com.au{url}"
                
            description = desc_elem.get_text().strip() if desc_elem else ""
            
            # Parse date if available
            pub_date = None
            if date_elem:
                date_str = date_elem.get('datetime') or date_elem.get_text().strip()
                try:
                    pub_date = datetime.fromisoformat(date_str)
                    pub_date = pub_date.astimezone(pytz.UTC)
                except (ValueError, TypeError):
                    pub_date = datetime.utcnow()
            else:
                pub_date = datetime.utcnow()
                
            return {
                'title': title,
                'url': url,
                'description': description,
                'pub_date': pub_date.isoformat()
            }
        except Exception as e:
            print(f"Error parsing article: {e}")
            return None
    
    def parse_page(self, html_content: str) -> List[Dict[str, str]]:
        """
        Parse articles from a news page.
        
        Args:
            html_content: HTML content of the page.
            
        Returns:
            List of article dictionaries.
        """
        articles = []
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            # Note: This selector will need to be updated based on actual AFL.com.au HTML structure
            article_elements = soup.find_all('article')
            
            for article_elem in article_elements:
                article_data = self.parse_article(article_elem)
                if article_data:
                    articles.append(article_data)
        except Exception as e:
            print(f"Error parsing page: {e}")
            
        return articles
    
    def extract_next_page_url(self, html_content: str) -> Optional[str]:
        """
        Extract the URL of the next page if available.
        
        Args:
            html_content: HTML content of the current page.
            
        Returns:
            URL of next page if available, None otherwise.
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            # Note: This selector will need to be updated based on actual AFL.com.au HTML structure
            next_link = soup.find('a', {'rel': 'next'}) or soup.find('a', text='Next')
            if next_link:
                url = next_link.get('href', '')
                if not url.startswith('http'):
                    url = f"https://www.afl.com.au{url}"
                return url
        except Exception as e:
            print(f"Error extracting next page URL: {e}")
        return None
    
    def scrape_articles(self) -> List[Dict[str, str]]:
        """
        Scrape articles from AFL.com.au news pages.
        
        Returns:
            List of article dictionaries.
        """
        all_articles = []
        current_url = self.BASE_URL
        pages_scraped = 0
        
        while current_url and pages_scraped < self.max_pages:
            html_content = self.fetch_page(current_url)
            if not html_content:
                break
                
            articles = self.parse_page(html_content)
            all_articles.extend(articles)
            
            pages_scraped += 1
            if pages_scraped >= self.max_pages:
                break
                
            current_url = self.extract_next_page_url(html_content)
            
        return all_articles 