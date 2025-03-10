# AFL.com.au RSS Feed Generator

A Python application that generates an RSS feed for AFL.com.au news articles. The application scrapes the AFL website daily, filters content based on configurable criteria, and generates a standard RSS 2.0 feed that can be consumed by any RSS reader.

## Features

- Daily scraping of AFL.com.au news articles
- Configurable content filtering (URL patterns and title keywords)
- Automatic exclusion of AFLW articles by default
- Standard RSS 2.0 feed generation
- Duplicate article prevention
- Automated execution via GitHub Actions
- Feed delivery via GitHub Pages

## Installation

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Configuration

The application uses a `config.yml` file for configuration. Example configuration:

```yaml
filters:
  url_patterns:
    - "/aflw/"  # Exclude AFLW articles
  title_keywords:
    - "AFLW"    # Exclude articles with AFLW in title
```

## Usage

The application runs automatically via GitHub Actions on a daily schedule. You can also run it manually:

```bash
python src/main.py
```

The generated RSS feed will be available at your GitHub Pages URL. 