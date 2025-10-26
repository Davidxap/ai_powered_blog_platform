from django import forms
from blog.models import Category


class AIArticleForm(forms.Form):
    """
    Form for AI article generation with category selection
    """
    keyword = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter main topic or keyword"
        }),
        help_text="Main topic for the article"
    )
    
    language = forms.ChoiceField(
        choices=[
            ("en", "English"),
            ("es", "Spanish"),
        ],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
    tone = forms.CharField(
        max_length=100,
        initial="professional, informative",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text="e.g., professional, casual, technical"
    )
    
    target_audience = forms.CharField(
        max_length=100,
        initial="general readers",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text="Who is this article for?"
    )
    
    min_words = forms.IntegerField(
        initial=800,
        min_value=300,
        max_value=5000,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    
    max_words = forms.IntegerField(
        initial=1200,
        min_value=300,
        max_value=5000,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    
    # Category selection from existing categories
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all().order_by("name"),
        required=True,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select one or more categories for this article"
    )
