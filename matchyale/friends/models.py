from django.db import models
from django.contrib.auth.models import User




class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)

    @classmethod
    def add_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def remove_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

    @classmethod
    def get_all_friends(cls, current_user):
        return cls.objects.filter(current_user = current_user)
    
class FriendRequest(models.Model):
    sender=models.ForeignKey(User,null=True,related_name='senders',on_delete=models.CASCADE)
    receiver=models.ForeignKey(User,null=True,related_name = 'receivers', on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.sender} send to {self.receiver}'
        

        
