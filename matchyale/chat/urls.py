from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="chat-home"),
    path("<str:username>/", views.private_chat, name="chat"),
    path("group/public/", views.public_room, name="group-chat"),
]