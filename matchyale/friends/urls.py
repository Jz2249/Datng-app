from django.urls import path, include
from .views import FriendView
from . import views
urlpatterns = [
    path('relationship/', FriendView.as_view(), name='my-relationship'),
    path('change_relationship/<str:operation>/<int:pk>', views.change_friends, name='my-removal'),
    path('my_request/<int:pk>', views.friend_request, name='my-request'),
    path('change_relationship/<str:operation>/<int:pk>', views.change_friends, name='my-add'),
    path('remove_request/<str:operation>/<int:pk>', views.remove_request, name='my-request-removal'),
]