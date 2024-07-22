
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogHome, name='blogHome'),
    path('postComment', views.postComment, name='postComment'),
    path('<str:slug>', views.blogPost, name='blogPost'),
    path('search/', views.search_blogs, name='search_blogs'),
]


'''
urlpatterns = [
    path('', views.blogHome, name='blogHome'),
    path('post/<slug:slug>/', views.blogPost, name='blogPost'),
    path('post_comment/', views.postComment, name='postComment'),
    path('create_post/', views.create_post, name='create_post'),
    path('search/', views.search_blogs, name='search_blogs'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
]'''
