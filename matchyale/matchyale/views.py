from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.models import Profile
from django.contrib.auth.models import User
from friends.models import FriendRequest
from operator import itemgetter

def home_view(request, *args, **kwargs):
    """
    Homepage has default interface.
    If user chooses to serach others, it will redirect to user's infomation. (only basic info will be showed to user without login)
    """
    # print(request)
    top3_list = []
    top3_dict = {}
    top3_num = []
    for user in User.objects.all():     
        received_requests = FriendRequest.objects.filter(receiver=user)
        top3_list.append(user)
        top3_num.append(received_requests.count())
        top3_dict.update({str(user): received_requests.count()})
    print(top3_dict)
    top3_list =sorted(top3_list,  key=lambda x: top3_dict[str(x)], reverse=True)
    print(top3_list)
    top3_num = sorted(top3_num, reverse=True)[:3]
    top3_list = top3_list[:3]
    try:
        top1 = top3_list[0]
        top1_num = top3_num[0]
    except:
        top1 = None
        top1_num = None
    try:
        top2 = top3_list[1]
        top2_num = top3_num[1]
    except:
        top2 = None
        top2_num = None
    try:
        top3 = top3_list[2]
        top3_num = top3_num[2]
    except:
        top3 = None
        top3_num = None
    context = {
        'top1_user': top1,
        'top2_user': top2,
        'top3_user': top3,
        'top1_num': top1_num,
        'top2_num': top2_num,
        'top3_num': top3_num
    }
    query_dict = request.GET
    try:
        query = (query_dict.get('q')) # key is 'q'
        if not request.user.is_authenticated: ### TODO should have error msg indicating "login needed", better raise exception here
            return redirect('/login')
    except Exception:
        print("error pageee") ### TODO should have error page showing invalid search
        return render(request, 'home.html', context)
    # print(query)
    user = None
    if not query:
         return render(request, 'home.html', context)
    else :
        try:
            user = User.objects.get(username=query)
        except Exception:
            print("error page") ### TODO should have error page showing none existed user
            return render(request, 'home.html') 
        return redirect(f'userinfo/{user.username}')  # user can search for user's basic information before login in homepage (default search)


    
    