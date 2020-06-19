from django.urls import path
from .views import PostUpdateView, UserPostListView
from . import views
import re

app_name = 'crop'
urlpatterns = [
    path('', views.home, name='home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/new/', views.post_create, name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post-delete'),
    path('buy/<int:pk>/', views.buy, name='buy'),
]