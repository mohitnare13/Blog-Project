from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from django.utils import timezone
from .forms import PostForm, BlogSearchForm
import requests
from django.http import Http404


def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, "blog/blogHome.html", context)

def blogPost(request, slug):
    # Use get_object_or_404 to fetch the post or return 404 if not found
    post = get_object_or_404(Post, slug=slug)
    
    # Increment the views count
    post.views = post.views + 1
    post.save()
    
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context = {'post': post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, "blog/blogPost.html", context)

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
        
    return redirect(f"/blog/{post.slug}")

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')  # Replace with your desired redirect URL name
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def article_detail(request, index):
    try:
        article = Post.objects.all()[index]
    except IndexError:
        raise Http404("Article not found")

    context = {'article': article}
    return render(request, 'blog/article_detail.html', context)


def search_blogs(request):
    form = BlogSearchForm(request.GET or None)
    articles = []

    if form.is_valid():
        query = form.cleaned_data['query']

        # Search in the local database
        posts = Post.objects.filter(title__icontains=query)

        if posts.exists():
            articles = posts
        else:
            # Fetch from API
            url = 'https://newsapi.org/v2/everything'
            params = {
                'q': query,
                'apiKey': 'afff08355cda478490b6cef541c61ee9',
                'sortBy': 'publishedAt',
                'language': 'en',
                'pageSize': 10
            }
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                request.session['fetched_articles'] = articles
            else:
                error_message = f"API request failed with status code {response.status_code}"
                messages.error(request, error_message)

    return render(request, 'blog/search_results.html', {'form': form, 'articles': articles})