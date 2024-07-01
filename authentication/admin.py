from django.contrib import admin

from .models import InviteCode, User

# Register your models here.
admin.site.register(User)
admin.site.register(InviteCode)
