# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a web scraping application built with Streamlit and Selenium. It provides a web interface for scraping websites and displaying the HTML content.

## Common Commands

### Running the Application
```bash
streamlit run main.py
```

### Installing Dependencies
```bash
# Using conda Python (default for this environment)
/opt/anaconda3/bin/pip install -r requirements.txt

# Or using system Python
pip install -r requirements.txt
```

## Architecture

### Core Components

1. **main.py**: Streamlit application entry point
   - Provides web UI for URL input
   - Handles user interactions and error display
   - Shows scraped HTML content with truncation for large pages

2. **scraper.py**: Web scraping implementation
   - Uses Selenium WebDriver with Chrome
   - Runs in headless mode for performance
   - Auto-installs ChromeDriver via webdriver-manager if needed
   - Returns raw HTML content from target websites

### Key Design Decisions

- **Headless Chrome**: The scraper runs Chrome in headless mode with flags `--no-sandbox`, `--disable-dev-shm-usage`, and `--disable-gpu` for compatibility across different environments
- **Auto-driver Management**: Uses webdriver-manager to automatically handle ChromeDriver installation and updates
- **Dynamic Content Support**: Includes a 3-second wait to allow JavaScript-rendered content to load

## Environment Notes

- Python environment: `/opt/anaconda3/bin/python` (Anaconda)
- Claude permissions are configured in `.claude/settings.local.json` to allow Python and pip commands