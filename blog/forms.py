from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts
    """
    class Meta:
        model = Post
        fields = ["title", "body", "categories"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
            "categories": forms.CheckboxSelectMultiple(),
        }
    
    def clean_categories(self):
        """
        Ensure at least one category is selected
        """
        categories = self.cleaned_data.get("categories")
        if not categories or categories.count() == 0:
            raise forms.ValidationError("Please select at least one category.")
        return categories


class CommentForm(forms.Form):
    """
    Form for creating comments
    """
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Your comment", "rows": 4}
        )
    )
