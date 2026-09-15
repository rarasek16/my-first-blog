from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import PostForm
from .models import Category, Post


def navigation_context():
    return {"categories": Category.objects.all()}


def post_list(request, category_slug=None):
    posts = (
        Post.objects.filter(published_date__lte=timezone.now())
        .select_related("author", "category")
        .order_by("-published_date")
    )
    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=selected_category)

    return render(
        request,
        "blog/post_list.html",
        {
            **navigation_context(),
            "posts": posts,
            "selected_category": selected_category,
        },
    )


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, published_date__lte=timezone.now())
    return render(request, "blog/post_detail.html", {**navigation_context(), "post": post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.published_date is None:
                post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
    return render(
        request,
        "blog/post_edit.html",
        {**navigation_context(), "form": form, "is_edit": False},
    )


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.published_date is None:
                post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(
        request,
        "blog/post_edit.html",
        {**navigation_context(), "form": form, "is_edit": True, "post": post},
    )


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)
