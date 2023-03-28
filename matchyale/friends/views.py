from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin   
from .models import  Friend, FriendRequest
# Create your views here.
class FriendView(LoginRequiredMixin,TemplateView):
    template_name = 'friends/relationship.html'

    def get(self, request):
        try:
            friend = Friend.objects.filter(current_user=request.user).first()

            print(f"current_user is {friend}")
        except:
            friend = None
        try:
            friends = friend.users.all()
            print(f"friends is {friends}")
            friends_number = friends.count()
        except:
            friends = []
            friends_number = 0
        all_users = User.objects.all()
        try:
            received_requests = User.objects.get(id=request.user.id).receivers.all()
        except:
            received_requests = []
        try:
            sent_requests = User.objects.get(id=request.user.id).senders.all()
        except:
            sent_requests = []
        received_num = len(received_requests)
        sent_num = len(sent_requests)
        context = {
            'friends': friends,
            'friends_number': friends_number,
            'all_users': all_users,
            'received_requests': received_requests,
            'received_num': received_num,
            'sent_requests': sent_requests,
            'sent_num': sent_num,

        }
        return render(request, self.template_name, context)
       

@login_required
def change_friends(request, operation, pk):
    new_friend = User.objects.get(id=pk)
    if operation == 'add':
        friend_req = FriendRequest.objects.get(sender=new_friend, receiver=request.user)
        Friend.add_friend(request.user, new_friend)
        Friend.add_friend(new_friend, request.user)
        friend_req.delete()
    elif operation == 'remove':
        Friend.remove_friend(request.user, new_friend)
        Friend.remove_friend(new_friend, request.user)

    return redirect('my-relationship')
@login_required
def friend_request(request, pk):
    sender = request.user
    recipient = User.objects.get(id=pk)
    
    # make sure user cannot like himself and cannot repeat add someone who is already in friendlist
    friend = Friend.objects.filter(current_user=sender).first()
    if friend is not None:
        friends = friend.users.all()
    else: # new user should create a friendrequest object first
        friends = None
        if recipient.username != sender.username:
            friend_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=recipient)
    if friends is not None and recipient not in friends and recipient.username != sender.username:
        try: # check if there is already a friend request from the recipient
            sender.receivers.all().get(sender = recipient)
        except: # if didnt't receive friend request from the recipient, create a new friend request
            friend_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=recipient)
           
        else: # add them to each friend list and remove from received friend request
            Friend.add_friend(sender,  recipient)
            Friend.add_friend(recipient,  sender)
            remove_request(request, 'remove-received-requests', pk)

    return redirect('my-relationship')
@login_required
def remove_request(request, operation, pk):
    target_user = User.objects.get(id=pk)

    if operation == 'remove-sent-requests':
        print('#############')
        print(target_user)
        sent_request = FriendRequest.objects.get(sender=request.user, receiver=target_user)
        sent_request.delete()
    elif operation == 'remove-received-requests':
        received_request = FriendRequest.objects.get(sender=target_user, receiver=request.user)
        received_request.delete()
    return redirect('my-relationship')






