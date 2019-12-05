from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home_view, name='home_view'),
    path('blog/', blog_view, name='blog_view'),
    path('post/<int:pk>/', PostView.as_view(), name='post_view'),
    path('newpost/', CreatePostView.as_view(success_url='/blog/'), name='create_post_view'),
    path('delete/<int:pk>/', DeletePostView.as_view(), name='delete_view'),
]
