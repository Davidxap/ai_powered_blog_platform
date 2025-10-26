"""
AI Article Generation utilities
Generates plain text articles using OpenAI API
"""
import logging
from typing import Dict
import requests
from openai import OpenAI

logger = logging.getLogger(__name__)


class ArticleGenerator:
    """
    Handles AI-powered article generation using OpenAI API
    Output: plain text, well-structured
    """
    
    def __init__(self, openai_key: str, valueserp_key: str):
        self.client = OpenAI(api_key=openai_key)
        self.valueserp_key = valueserp_key
        self.model = "gpt-4o-mini"
    
    def generate_article(self, keyword: str, language: str = "en", 
                        tone: str = "professional", target_audience: str = "general",
                        min_words: int = 800, max_words: int = 1200,
                        country: str = "us") -> str:
        """
        Generate plain text article based on parameters
        
        Args:
            keyword: Main topic/keyword
            language: Target language (en, es)
            tone: Writing tone
            target_audience: Intended audience
            min_words: Minimum word count
            max_words: Maximum word count
            country: Country code for search context
            
        Returns:
            Plain text article content
        """
        # Search context from web
        context = self._search_context(keyword, country, language)
        
        # Build prompt
        prompt = self._build_prompt(
            keyword, language, tone, target_audience,
            min_words, max_words, context
        )
        
        # Generate via OpenAI
        article_text = self._generate_with_openai(prompt, language)
        
        return article_text
    
    def _search_context(self, keyword: str, country: str, lang: str) -> Dict:
        """
        Search web for context using ValueSerp API
        Returns overview and URLs
        """
        context = {"overview": "", "urls": []}
        
        try:
            response = requests.get(
                "https://api.valueserp.com/search",
                params={
                    "api_key": self.valueserp_key,
                    "q": keyword,
                    "hl": lang,
                    "gl": country,
                    "num": 5
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Get answer box if available
                if answer_box := data.get("answer_box"):
                    context["overview"] = (
                        answer_box.get("answer") or 
                        answer_box.get("snippet") or ""
                    )[:600]
                
                # Get top URLs
                organic = data.get("organic_results", [])[:3]
                context["urls"] = [r["link"] for r in organic if r.get("link")]
                
        except Exception as e:
            logger.warning(f"Search error for '{keyword}': {e}")
        
        return context
    
    def _build_prompt(self, keyword: str, language: str, tone: str,
                    audience: str, min_words: int, max_words: int,
                    context: Dict) -> str:
        """
        Build prompt for plain text article with localized title
        """
        context_str = f"Search context: {context.get('overview', 'N/A')}"

        prompt = f"""You are an expert blog writer and SEO specialist.

    Write a complete, well-structured blog article about: "{keyword}"

    CRITICAL REQUIREMENT:
    - The FIRST LINE of your output must be the article title in {language}
    - If the keyword is in a different language, translate or adapt the title naturally to {language}
    - The title should be clear, engaging, and appropriate for the target language

    REQUIREMENTS:
    - Language: {language} (all content must be in this language)
    - Tone: {tone}
    - Target audience: {audience}
    - Word count: {min_words}-{max_words} words
    - Format: PLAIN TEXT ONLY (no HTML, no Markdown, no special formatting)

    STRUCTURE:
    - Line 1: Article title in {language} (clear, natural translation/adaptation of the keyword)
    - Line 2: Empty line
    - Line 3+: Article content with clear sections and paragraphs

    CONTENT GUIDELINES:
    - Be informative, accurate, and engaging
    - Include practical examples
    - Maintain consistent tone throughout
    - Natural keyword integration
    - Write naturally in {language}

    {context_str}

    Return ONLY the article text starting with the title. No explanations, no metadata."""

        return prompt

    
    def _generate_with_openai(self, prompt: str, language: str) -> str:
        """
        Call OpenAI API to generate plain text article
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional {language} content writer. Always write ONLY in {language}. Return plain text, well-structured for a blog."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            # Safe extraction
            message_content = response.choices[0].message.content
            
            if message_content is None:
                raise ValueError("OpenAI returned empty content")
            
            article = message_content.strip()
            return article
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise Exception(f"Failed to generate article: {str(e)}")
