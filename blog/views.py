from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Category
from .forms import CommentForm, PostForm  # ← Importar ambos formularios


# Create your views here.

def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
    }
    return render(request, "blog/index.html", context)


def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)

        if request.user.is_authenticated:
            if form.is_valid():
                comment = Comment(
                    author=request.user,
                    body=form.cleaned_data["body"],
                    post=post,
                )
                comment.save()
                return HttpResponseRedirect(request.path_info)
        else:
            return HttpResponseRedirect("/accounts/login/")

    comments = Comment.objects.filter(post=post).order_by("-created_on")

    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }
    return render(request, "blog/detail.html", context)


@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST["title"]
        body = request.POST["body"]
        post = Post.objects.create(author=request.user, title=title, body=body)
        return redirect("blog_detail", pk=post.pk)
    return render(request, "blog/create_post.html")


@login_required
def dashboard_view(request):
    user_posts = Post.objects.filter(author=request.user).order_by("-created_on")
    
    context = {
        "user": request.user,
        "user_posts": user_posts,
    }
    return render(request, "dashboard/dashboard.html", context)


@login_required
def create_post_view(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect("dashboard")
    else:
        form = PostForm()
    
    return render(request, "dashboard/create_post.html", {"form": form})
