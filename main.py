import streamlit as st
from scraper import scrape_website

st.set_page_config(page_title="AI Web Scraper")
st.title("AI Web Scraper")

url = st.text_input("Enter the URL of the website to scrape:")

if st.button("Scrape Site"):
    if not url:
        st.warning("Please enter a URL to scrape.")
    else:
        st.info("Scraping the website...")
        try:
            with st.spinner("Scraping in progress..."):
                result = scrape_website(url)
            st.success("Scrape finished.")
            # show the raw HTML or a truncated preview in the app
            if result:
                preview = result[:1000]
                st.code(preview, language="html")
                if len(result) > len(preview):
                    st.write(f"... (truncated, {len(result)} total characters)")
            else:
                st.info("No content returned from scraper.")
        except Exception as e:
            st.error(f"Error scraping website: {e}")