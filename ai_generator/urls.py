from django.urls import path
from . import views

urlpatterns = [
    path("generate/", views.generate_article_view, name="generate_article"),
]
