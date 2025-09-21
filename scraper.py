import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


def scrape_website(website_url):
    """Launch Chrome, navigate to website_url and return page HTML."""
    print("Launching Browser...")

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

        driver.get(website_url)
        print("Website loaded successfully.")

        time.sleep(3)

        html_content = driver.page_source
        return html_content

    except Exception as e:
        print(f"Error during scraping: {e}")
        raise
    finally:
        if driver:
            driver.quit()