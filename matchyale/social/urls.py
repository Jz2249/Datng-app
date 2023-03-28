from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, CommentDeleteView
from . import views

urlpatterns = [
    path('moment/<int:post_pk>/comment/delete/<int:pk>', CommentDeleteView.as_view(), name='comment-delete'),
    path('moment', PostListView.as_view(), name='moment-home'),
    path('moment/<int:pk>/', PostDetailView.as_view(), name='moment-detail'),
    path('moment/<int:pk>/update', PostUpdateView.as_view(), name='moment-update'),
    path('moment/<int:pk>/delete', PostDeleteView.as_view(), name='moment-delete'),
    path('moment/new', PostCreateView.as_view(), name='moment-new'),
    path('userinfo/<str:username>', views.get_user_profile, name='user-info2'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-info'),
]
