from django.shortcuts import render
from django.contrib.auth.models import User
from friends.models import Friend
# Create your views here.

from .models import ChatMessage

def index(request):
    # users = Friend.objects.exclude(current_user=request.user.id)
    # users = Friend.objects.filter(current_user=request.user).first().users.all()
    users = request.user
    context = {
        'users': users
    }
    return render(request, "chat/index.html", context)


def private_chat(request, username):

    user = User.objects.get(username=username) # receiver
    friends = Friend.objects.filter(current_user=request.user).first().users.all()
    if request.user.id > user.id:
        room_name = f'chat_{request.user.id}-{user.id}'
    else:
        room_name = f'chat_{user.id}-{request.user.id}'
    length = len(ChatMessage.objects.filter(room_name=room_name))
    if (length < 10):
        message = ChatMessage.objects.filter(room_name=room_name)
    else:
        message = ChatMessage.objects.filter(room_name=room_name)[length - 10: length]
    return render(request, 'chat/private_chat.html', context={'user': user, "room_name": room_name, 'messages': message, 'friends': friends})




def public_room(request):
    username = request.GET.get('username', 'Anonymous')
    # messages = ChatMessage.objects.filter(room_name=room_name)[0:25]

    return render(request, 'chat/public_room.html', { 'username': username})