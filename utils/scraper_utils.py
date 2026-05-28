import requests
from bs4 import BeautifulSoup
import re


def clean_text(text):
    """Basic text cleaning - remove extra whitespace"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def normalize_topics(topic_list):
    """Normalize topic names - remove duplicates, standardize formatting"""
    normalized = []
    seen = set()
    for topic in topic_list:
        cleaned = clean_text(topic).lower()
        if cleaned not in seen and cleaned:
            seen.add(cleaned)
            normalized.append(clean_text(topic))
    return normalized


def remove_duplicates(items, key=None):
    """Remove duplicate items from a list, optionally using a key"""
    seen = set()
    result = []
    for item in items:
        if key:
            item_key = str(key(item))
        else:
            item_key = str(item)
        if item_key not in seen:
            seen.add(item_key)
            result.append(item)
    return result


def clean_pdf_noise(text):
    """Clean common PDF noise - page numbers, headers, footers, etc."""
    # Remove page numbers
    text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^\d+$', '', text, flags=re.MULTILINE)
    
    # Remove common headers/footers
    text = re.sub(r'KPSC|Karnataka Public Service Commission', '', text, flags=re.IGNORECASE)
    
    # Remove extra newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return clean_text(text)


def filter_irrelevant_content(text, irrelevant_keywords=None):
    """Filter out irrelevant content based on keywords"""
    if not irrelevant_keywords:
        irrelevant_keywords = [
            'jee', 'rbi', 'tnpsc', 'mp si', 'mahatet', 
            'rajasthan', 'banking', 'engineering', 'medical',
            'upsc', 'ias', 'ips', 'ifs'
        ]
    text_lower = text.lower()
    for keyword in irrelevant_keywords:
        if keyword.lower() in text_lower:
            return ""
    return text


def extract_links(soup, base_url=""):
    """Extract all valid links from a BeautifulSoup object"""
    links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if not href.startswith('http') and base_url:
            href = base_url + href
        links.append(href)
    return links


def get_soup(url, timeout=15):
    """Get BeautifulSoup object from a URL"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')
