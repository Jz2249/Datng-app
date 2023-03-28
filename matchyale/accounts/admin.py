from django.contrib import admin

# Register your models here.
from .models import Profile

class AccountAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
    search_fields = ["id", "gender"]
admin.site.register(Profile)
