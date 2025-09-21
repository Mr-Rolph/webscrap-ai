import os
import json
from openai import OpenAI


class WebsiteAnalyzer:
    def __init__(self, api_key=None):
        """Initialize the analyzer with OpenAI API key."""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def analyze_content(self, scraped_data, user_prompt):
        """Analyze scraped website content based on user prompt."""

        if not self.client:
            return "Please set your OpenAI API key in the environment variable OPENAI_API_KEY or pass it directly."

        # Prepare context from scraped data
        context = self._prepare_context(scraped_data)

        # Create the system and user messages
        system_message = """You are a helpful assistant that analyzes website content.
        You have been provided with scraped data from a website including its title,
        description, headings, text content, links, and images.
        Answer the user's questions based solely on this scraped information."""

        user_message = f"""Based on the following website data, please answer this question: {user_prompt}

Website Data:
{context}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=500
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error calling OpenAI API: {str(e)}"

    def _prepare_context(self, scraped_data):
        """Prepare a concise context from scraped data for the AI."""

        context_parts = []

        # Add title and description
        context_parts.append(f"Title: {scraped_data.get('title', 'N/A')}")
        context_parts.append(f"Description: {scraped_data.get('meta_description', 'N/A')}")

        # Add main headings
        headings = scraped_data.get('headings', {})
        if headings:
            all_headings = []
            for level in ['h1', 'h2', 'h3']:
                if level in headings:
                    all_headings.extend(headings[level][:5])  # Top 5 of each level
            if all_headings:
                context_parts.append(f"Main Headings: {', '.join(all_headings[:10])}")

        # Add text preview
        text_content = scraped_data.get('text_content', '')
        if text_content:
            context_parts.append(f"Content Preview: {text_content[:500]}...")

        # Add first few paragraphs
        paragraphs = scraped_data.get('paragraphs', [])
        if paragraphs:
            context_parts.append(f"Key Paragraphs: {' '.join(paragraphs[:2])}")

        # Add link count and sample links
        links = scraped_data.get('links', [])
        if links:
            context_parts.append(f"Total Links: {len(links)}")
            sample_links = [f"{link['text']}" for link in links[:5]]
            context_parts.append(f"Sample Link Texts: {', '.join(sample_links)}")

        # Add image info
        images = scraped_data.get('images', [])
        if images:
            context_parts.append(f"Total Images: {len(images)}")
            sample_alts = [img['alt'] for img in images[:3] if img['alt'] != 'No alt text']
            if sample_alts:
                context_parts.append(f"Sample Image Descriptions: {', '.join(sample_alts)}")

        return '\n'.join(context_parts)