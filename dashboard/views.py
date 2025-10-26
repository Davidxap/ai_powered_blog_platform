from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from blog.models import Post, Comment, Category
from blog.forms import PostForm


@login_required
def dashboard_view(request):
    """
    Main dashboard view with user statistics and recent posts
    """
    # Get all posts created by the logged-in user
    user_posts = Post.objects.filter(author=request.user).order_by("-created_on")
    
    # Calculate user statistics
    user_posts_count = user_posts.count()
    total_comments = Comment.objects.filter(post__author=request.user).count()
    categories_used = user_posts.values('categories').distinct().count()
    
    context = {
        "user": request.user,
        "user_posts": user_posts[:10],  # Show last 10 posts
        "user_posts_count": user_posts_count,
        "total_comments": total_comments,
        "categories_used": categories_used,
    }
    return render(request, "dashboard/dashboard.html", context)


@login_required
def edit_post_view(request, pk):
    """
    Edit an existing post
    Only the post author can edit their own posts
    """
    # Get post and verify ownership
    post = get_object_or_404(Post, pk=pk)
    
    # Security check: only author can edit
    if post.author != request.user:
        messages.error(request, "You don't have permission to edit this post.")
        return HttpResponseForbidden("You are not authorized to edit this post.")
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # Save post without committing to database yet
            updated_post = form.save(commit=False)
            # Ensure author remains the same
            updated_post.author = request.user
            updated_post.save()
            # Save many-to-many relationships (categories)
            form.save_m2m()
            
            messages.success(request, f"Post '{post.title}' updated successfully!")
            return redirect("blog_detail", pk=post.pk)
    else:
        # Pre-populate form with existing post data
        form = PostForm(instance=post)
    
    context = {
        "form": form,
        "post": post,
        "is_edit": True
    }
    return render(request, "dashboard/post_form.html", context)


@login_required
def delete_post_view(request, pk):
    """
    Delete a post
    Only the post author can delete their own posts
    """
    # Get post and verify ownership
    post = get_object_or_404(Post, pk=pk)
    
    # Security check: only author can delete
    if post.author != request.user:
        messages.error(request, "You don't have permission to delete this post.")
        return HttpResponseForbidden("You are not authorized to delete this post.")
    
    if request.method == "POST":
        # Delete the post (comments will be deleted automatically due to CASCADE)
        post_title = post.title
        post.delete()
        messages.success(request, f"Post '{post_title}' deleted successfully.")
        return redirect("dashboard")
    
    # Show confirmation page for GET request
    context = {"post": post}
    return render(request, "dashboard/confirm_delete_post.html", context)


@login_required
def edit_comment_view(request, pk):
    """
    Edit a comment
    Only the comment author can edit their own comments
    """
    # Get comment and verify ownership
    comment = get_object_or_404(Comment, pk=pk)
    
    # Security check: only author can edit
    if comment.author != request.user:
        messages.error(request, "You don't have permission to edit this comment.")
        return HttpResponseForbidden("You are not authorized to edit this comment.")
    
    if request.method == "POST":
        # Get new comment text from form
        new_body = request.POST.get("body", "").strip()
        
        if new_body:
            # Update comment
            comment.body = new_body
            comment.save()
            messages.success(request, "Comment updated successfully!")
        else:
            messages.error(request, "Comment cannot be empty.")
        
        # Redirect back to the post
        return redirect("blog_detail", pk=comment.post.pk)
    
    # Show edit form for GET request
    context = {"comment": comment}
    return render(request, "dashboard/edit_comment.html", context)


@login_required
def delete_comment_view(request, pk):
    """
    Delete a comment
    Only the comment author can delete their own comments
    """
    # Get comment and verify ownership
    comment = get_object_or_404(Comment, pk=pk)
    
    # Security check: only author can delete
    if comment.author != request.user:
        messages.error(request, "You don't have permission to delete this comment.")
        return HttpResponseForbidden("You are not authorized to delete this comment.")
    
    # Store post pk before deleting comment
    post_pk = comment.post.pk
    
    if request.method == "POST":
        # Delete the comment
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect("blog_detail", pk=post_pk)
    
    # Show confirmation page for GET request
    context = {"comment": comment}
    return render(request, "dashboard/confirm_delete_comment.html", context)

@login_required
def create_post_view(request):
    """
    Create a new blog post with category selection
    """
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # Save post without committing to database yet
            post = form.save(commit=False)
            # Set the author as the logged-in user
            post.author = request.user
            post.save()
            # Save many-to-many relationships (categories)
            form.save_m2m()
            
            messages.success(request, f"Post '{post.title}' created successfully!")
            return redirect("blog_detail", pk=post.pk)
    else:
        # Show empty form
        form = PostForm()
    
    context = {
        "form": form,
        "is_edit": False
    }
    return render(request, "dashboard/post_form.html", context)