from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .forms import AIArticleForm
from .ai_utils import ArticleGenerator
from blog.models import Post
import logging

logger = logging.getLogger(__name__)


@login_required
def generate_article_view(request):
    """
    View to generate AI-powered articles with localized title
    """
    if request.method == "POST":
        form = AIArticleForm(request.POST)
        
        if form.is_valid():
            # Extract all user inputs
            keyword = form.cleaned_data["keyword"]
            language = form.cleaned_data["language"]
            tone = form.cleaned_data["tone"]
            target_audience = form.cleaned_data["target_audience"]
            min_words = form.cleaned_data["min_words"]
            max_words = form.cleaned_data["max_words"]
            selected_categories = form.cleaned_data["categories"]
            
            try:
                # Initialize AI generator
                generator = ArticleGenerator(
                    openai_key=settings.OPENAI_API_KEY,
                    valueserp_key=settings.VALUESERP_API_KEY
                )
                
                # Generate article (first line is title, rest is body)
                full_article = generator.generate_article(
                    keyword=keyword,
                    language=language,
                    tone=tone,
                    target_audience=target_audience,
                    min_words=min_words,
                    max_words=max_words,
                    country=settings.DEFAULT_COUNTRY
                )
                
                # Extract title (first line) and body (rest)
                lines = full_article.split('\n', 1)
                if len(lines) >= 2:
                    title = lines[0].strip()
                    body = lines[1].strip()
                else:
                    # Fallback if no line break
                    title = keyword
                    body = full_article
                
                # Create post with localized title
                post = Post.objects.create(
                    title=title,  # ← Localized title from AI
                    body=body,
                    author=request.user
                )
                
                # Assign categories
                post.categories.set(selected_categories)
                post.save()
                
                messages.success(
                    request, 
                    f"Article '{title}' generated successfully!"
                )
                return redirect("blog_detail", pk=post.pk)
                
            except Exception as e:
                logger.error(f"Article generation failed: {e}")
                messages.error(
                    request, 
                    f"Failed to generate article: {str(e)}"
                )
        
    else:
        form = AIArticleForm()
    
    context = {"form": form}
    return render(request, "ai_generator/generate.html", context)
