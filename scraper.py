import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def scrape_website(url):
    """Scrape website and extract structured data."""

    # Ensure URL has protocol
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    print(f"Launching Browser for URL: {url}")

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = None
    try:
        try:
            driver = webdriver.Chrome(options=options)
        except WebDriverException:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        print("Website loaded successfully.")

        time.sleep(3)

        html_content = driver.page_source

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'lxml')

        # Extract structured data
        data = extract_page_data(soup, url)

        return data

    except Exception as e:
        print(f"Error during scraping: {e}")
        raise
    finally:
        if driver:
            driver.quit()


def extract_page_data(soup, base_url):
    """Extract structured data from the parsed HTML."""

    
    for script in soup(["script", "style"]):
        script.decompose()

    data = {
        'title': extract_title(soup),
        'meta_description': extract_meta_description(soup),
        'headings': extract_headings(soup),
        'paragraphs': extract_paragraphs(soup),
        'links': extract_links(soup, base_url),
        'images': extract_images(soup, base_url),
        'text_content': extract_text_content(soup)
    }

    return data


def extract_title(soup):
    """Extract page title."""
    title = soup.find('title')
    return title.get_text(strip=True) if title else 'No title found'


def extract_meta_description(soup):
    """Extract meta description."""
    meta = soup.find('meta', attrs={'name': 'description'})
    if meta and meta.get('content'):
        return meta['content']
    return 'No meta description found'


def extract_headings(soup):
    """Extract all headings (h1-h6)."""
    headings = {}
    for i in range(1, 7):
        h_tags = soup.find_all(f'h{i}')
        if h_tags:
            headings[f'h{i}'] = [h.get_text(strip=True) for h in h_tags[:10]] 
    return headings


def extract_paragraphs(soup):
    """Extract first 5 paragraphs with substantial text."""
    paragraphs = []
    for p in soup.find_all('p'):
        text = p.get_text(strip=True)
        if len(text) > 50:  
            paragraphs.append(text)
            if len(paragraphs) >= 5:
                break
    return paragraphs


def extract_links(soup, base_url):
    """Extract all links with their text."""
    links = []
    for link in soup.find_all('a', href=True)[:30]: 
        href = link['href']
        text = link.get_text(strip=True)

        # Make relative URLs absolute
        if not href.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            href = urljoin(base_url, href)

        if text:  # Only include links with text
            links.append({
                'text': text[:100],  # Limit text length
                'url': href
            })
    return links


def extract_images(soup, base_url):
    """Extract image URLs and alt text."""
    images = []
    for img in soup.find_all('img', src=True)[:20]:  # Limit to 20 images
        src = img['src']

        # Make relative URLs absolute
        if not src.startswith(('http://', 'https://', 'data:')):
            src = urljoin(base_url, src)

        images.append({
            'src': src,
            'alt': img.get('alt', 'No alt text')
        })
    return images


def extract_text_content(soup):
    """Extract clean text content from the page."""
    text = soup.get_text(separator=' ', strip=True)
    # Clean up excessive whitespace
    text = ' '.join(text.split())
    # Limit to first 1000 characters for preview
    return text[:1000] + '...' if len(text) > 1000 else text