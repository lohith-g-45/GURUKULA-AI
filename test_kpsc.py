from utils.scraper_utils import get_soup

url = "https://kpsc.kar.nic.in"
print(f"Fetching: {url}")
try:
    soup = get_soup(url)
    print("=" * 80)
    print("Page title:", soup.title.string if soup.title else "No title")
    print("=" * 80)
    print("\nAll headings (h1, h2, h3):")
    for tag in soup.find_all(['h1', 'h2', 'h3']):
        print(f"- {tag.name}: {tag.get_text(strip=True)}")
    print("\n" + "=" * 80)
    print("\nAll links (first 20):")
    for i, a in enumerate(soup.find_all('a', href=True)[:20]):
        print(f"{i+1}. {a.get_text(strip=True)[:50]} -> {a['href']}")
except Exception as e:
    print(f"Error: {e}")
