from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models import Q
from django.utils import timezone


class Profile(models.Model):
    class Meta:
        ordering = ['-created']
  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, default='', blank=True)

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    
    GENDER = (
        ('MAN', 'Man'),
        ('WOMAN', 'Woman'),
        ('NONBINARY', 'Nonbinary')
    )
    EDUCATION = (
        ('HIGH SCHOOL', 'High School'),
        ('UNDERGRAD', 'Undergrad'),
        ('POSTGRAD', 'Postgrad'),
        ('PREFER NOT TO SAY', 'Prefer not to say')
    )
    PRONOUNS = (
        ('HE/HIM/HIS', 'He/him/his'),
        ('SHE/HER/HERS', 'She/her/hers'),
        ('PREFER NOT TO SAY', 'Prefer not to say')
    )
    SEXUALITY = (
        ('PREFER NOT TO SAY', 'Prefer not to say'),
        ('STRAIGHT', 'Straight'),
        ('BISEXUAL', 'Bisexual'),
        ('GAY', 'Gay'),
        ('LESBIAN', 'Lesbian')
    )
    ETHNICITY = (
        ('EAST ASIAN', 'East Asian'),
        ('PREFER NOT TO SAY', 'Prefer not to say')
    )

    gender = models.CharField(choices=GENDER, default="MALE", max_length=10)
    pronouns = models.CharField(choices=PRONOUNS, default="HE/HIM/HIS", max_length=20)
    height = models.DecimalField(max_digits=10, default=180.34, decimal_places=2)
    education = models.CharField(choices=EDUCATION, default="HIGH SCHOOL", blank=False, max_length=100)
    birth_date = models.DateField(null=True, default='1990-01-01', blank=True)
    sexuality = models.CharField(choices=SEXUALITY, default="Straight", blank=False, max_length=20)
    ethnicity = models.CharField(choices=ETHNICITY, default="WHITE", blank=False, max_length=100)
    like_received = 0
    # Assistance from https://stackoverflow.com/questions/5056327/define-and-insert-age-in-django-template
    def age(self):
        return int((datetime.date.today() - self.birth_date).days / 365.25)
    def get_friends(self):
        return self.friends.all()
    def get_friends_number(self):
        return self.friends.all().count()
    
    def __str__(self):
        return f'{self.user.username} Profile'














