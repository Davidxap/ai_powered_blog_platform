from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("post/create/", views.create_post_view, name="create_post"),  # ← Esta línea
    path("post/edit/<int:pk>/", views.edit_post_view, name="edit_post"),
    path("post/delete/<int:pk>/", views.delete_post_view, name="delete_post"),
    path("comment/edit/<int:pk>/", views.edit_comment_view, name="edit_comment"),
    path("comment/delete/<int:pk>/", views.delete_comment_view, name="delete_comment"),
]
