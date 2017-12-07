# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm

def blog_home(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/blog_home.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})


@login_required
@staff_member_required
def blog_settings(request):
    posts = Post.objects.filter(published_date__lte=timezone.now(), author=request.user).order_by('published_date')
    no_posts = Post.objects.filter(published_date__isnull=True).order_by('published_date')
    return render(request, 'blog/blog_settings.html', {'posts': posts, 'no_posts': no_posts})


@login_required
@staff_member_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
@staff_member_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog_settings')


@login_required
@staff_member_required
def post_unpublish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.published_date = None
    post.save()
    return redirect('blog_settings')


@login_required
@staff_member_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
@staff_member_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog_settings')


@login_required
@staff_member_required
def comment_settings(request, pk):
    comments = Comment.objects.filter(post=pk)
    return render(request, 'blog/blog_comment_list.html', {'comments': comments})


@login_required
@staff_member_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog_settings')
