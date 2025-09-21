import streamlit as st
from scraper import scrape_website
from ai_analyzer import WebsiteAnalyzer
import json
import os

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
                data = scrape_website(url)

            st.success("Scrape finished.")

            # Store scraped data in session state for AI analysis
            st.session_state['scraped_data'] = data

            # Create tabs for different data types
            tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                "Overview", "Text Content", "Links", "Images", "Headings", "Raw Data", "AI Analysis"
            ])

            with tab1:
                st.subheader("Page Overview")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Page Title:**", data['title'][:50] + "..." if len(data['title']) > 50 else data['title'])
                with col2:
                    st.write("**Total Links Found:**", len(data['links']))

                st.write("**Meta Description:**")
                st.info(data['meta_description'])

                if data['paragraphs']:
                    st.write("**First Paragraph:**")
                    st.write(data['paragraphs'][0])

            with tab2:
                st.subheader("Text Content")
                st.write("**Clean Text Preview (first 1000 characters):**")
                st.text_area("", data['text_content'], height=300, disabled=True)

                if data['paragraphs']:
                    st.write("**Main Paragraphs:**")
                    for i, para in enumerate(data['paragraphs'], 1):
                        with st.expander(f"Paragraph {i}"):
                            st.write(para)

            with tab3:
                st.subheader(f"Links ({len(data['links'])} found)")
                if data['links']:
                    for link in data['links'][:20]:  # Show first 20
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            st.write(f"**{link['text']}**")
                        with col2:
                            st.code(link['url'], language=None)
                else:
                    st.info("No links found on this page.")

            with tab4:
                st.subheader(f"Images ({len(data['images'])} found)")
                if data['images']:
                    cols = st.columns(3)
                    for idx, img in enumerate(data['images'][:9]):  # Show first 9
                        with cols[idx % 3]:
                            st.write(f"**Alt:** {img['alt'][:50]}...")
                            st.code(img['src'][:100] + "..." if len(img['src']) > 100 else img['src'], language=None)
                            try:
                                if not img['src'].startswith('data:'):
                                    st.image(img['src'], use_container_width=True)
                            except:
                                st.write("*[Cannot display image]*")
                else:
                    st.info("No images found on this page.")

            with tab5:
                st.subheader("Page Headings Structure")
                if data['headings']:
                    for level, headings in sorted(data['headings'].items()):
                        st.write(f"**{level.upper()} Tags:**")
                        for heading in headings:
                            if level == 'h1':
                                st.markdown(f"# → {heading}")
                            elif level == 'h2':
                                st.markdown(f"## → {heading}")
                            elif level == 'h3':
                                st.markdown(f"### → {heading}")
                            else:
                                st.markdown(f"{'#' * int(level[1])} → {heading}")
                else:
                    st.info("No headings found on this page.")

            with tab6:
                st.subheader("Raw Scraped Data (JSON)")
                st.json(data)

                # Download button for the data
                json_str = json.dumps(data, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name=f"scraped_data_{url.replace('https://', '').replace('http://', '').replace('/', '_')[:30]}.json",
                    mime="application/json"
                )

            with tab7:
                st.subheader("AI Analysis")
                st.write("Ask questions about the scraped website content.")

                # Check for API key
                api_key = os.getenv('OPENAI_API_KEY')
                if not api_key:
                    st.warning("⚠️ OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
                    st.info("To set your API key, run: export OPENAI_API_KEY='your-key-here'")

                # Example questions section
                st.write("**💡 Example Questions You Can Ask:**")
                example_cols = st.columns(2)
                with example_cols[0]:
                    st.markdown("""
                    - What is this website about?
                    - What are the main topics covered?
                    - Summarize the key information
                    - What services are offered?
                    """)
                with example_cols[1]:
                    st.markdown("""
                    - Extract contact information
                    - What is the target audience?
                    - List the main features
                    - What makes this site unique?
                    """)

                # Prompt input with better styling
                st.write("**📝 Your Question:**")
                user_prompt = st.text_area(
                    "Enter your question about the website:",
                    placeholder="Type your question here... For example: 'What is the main purpose of this website?'",
                    height=100,
                    label_visibility="collapsed"
                )

                # Analyze button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    analyze_button = st.button("🤖 Analyze with AI", use_container_width=True)

                if analyze_button:
                    if not user_prompt:
                        st.warning("Please enter a question.")
                    elif not api_key:
                        st.error("Please set your OpenAI API key first.")
                    else:
                        with st.spinner("Analyzing with AI..."):
                            analyzer = WebsiteAnalyzer(api_key)
                            response = analyzer.analyze_content(data, user_prompt)

                        # Display response in a nice container
                        st.divider()
                        st.write("### 🎯 AI Response:")
                        response_container = st.container(border=True)
                        with response_container:
                            st.write(response)

                        # Add copy button for the response
                        st.text_area("Copy response:", response, height=100, label_visibility="collapsed", disabled=True)

        except Exception as e:
            st.error(f"Error scraping website: {e}")

# Display AI Analysis section if data exists in session state
elif 'scraped_data' in st.session_state:
    st.info("Previous scraped data found. You can analyze it with AI.")

    st.subheader("AI Analysis")
    st.write("Ask questions about the previously scraped website content.")

    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        st.warning("⚠️ OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        st.info("To set your API key, run: export OPENAI_API_KEY='your-key-here'")

    # Example questions section
    st.write("**💡 Example Questions You Can Ask:**")
    example_cols = st.columns(2)
    with example_cols[0]:
        st.markdown("""
        - What is this website about?
        - What are the main topics covered?
        - Summarize the key information
        - What services are offered?
        """)
    with example_cols[1]:
        st.markdown("""
        - Extract contact information
        - What is the target audience?
        - List the main features
        - What makes this site unique?
        """)

    # Prompt input with better styling
    st.write("**📝 Your Question:**")
    user_prompt = st.text_area(
        "Enter your question about the website:",
        placeholder="Type your question here... For example: 'What is the main purpose of this website?'",
        height=100,
        label_visibility="collapsed"
    )

    # Analyze button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button("🤖 Analyze with AI", use_container_width=True)

    if analyze_button:
        if not user_prompt:
            st.warning("Please enter a question.")
        elif not api_key:
            st.error("Please set your OpenAI API key first.")
        else:
            with st.spinner("Analyzing with AI..."):
                analyzer = WebsiteAnalyzer(api_key)
                response = analyzer.analyze_content(st.session_state['scraped_data'], user_prompt)

            # Display response in a nice container
            st.divider()
            st.write("### 🎯 AI Response:")
            response_container = st.container(border=True)
            with response_container:
                st.write(response)

            # Add copy button for the response
            st.text_area("Copy response:", response, height=100, label_visibility="collapsed", disabled=True)

# No data scraped yet - show welcome UI
else:
    st.markdown("### 👋 Welcome to AI Web Scraper")

    st.info("📌 **How to use:** Enter a URL above and click 'Scrape Site' to extract structured data from any website.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### ✨ Features
        - 🔍 Extract text, links, and images
        - 📊 View structured data in tabs
        - 💾 Download as JSON
        - 🤖 AI-powered analysis
        """)

    with col2:
        st.markdown("""
        #### 🎯 Use Cases
        - Research websites
        - Extract contact info
        - Analyze competitors
        - Content summarization
        """)

    st.divider()
    st.markdown("##### 🚀 Ready to start? Enter a URL above to begin scraping!")