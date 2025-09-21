import html
import time
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service

def scrape_website(website_url):
    print("Launching Browser...")

    chrome_driver_path = "./Google Chrome For Testing"  # Update this path as necessary
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    import html
    import time
    import selenium.webdriver as webdriver
    from selenium.webdriver.chrome.service import Service


    def scrape_website(website_url):
        print("Launching Browser...")

        chrome_driver_path = "./Google Chrome For Testing"  # Update this path as necessary
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

        import html
        import time
        import selenium.webdriver as webdriver
        from selenium.webdriver.chrome.service import Service


        def scrape_website(website_url):
            """Launch Chrome, navigate to website_url and return page HTML.

            Note: update chrome_driver_path to the exact chromedriver binary path.
            """
            print("Launching Browser...")

            chrome_driver_path = "./Google Chrome For Testing"  # Update this path as necessary
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

            try:
                driver.get(website_url)
                print("Website loaded successfully.")
                html_content = driver.page_source
                time.sleep(10)  # Wait for dynamic content to load

                return html_content
            finally:
                driver.quit()
