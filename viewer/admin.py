from django.contrib import admin

# Register your models here.

from viewer.models import Chatroom

admin.site.register([Chatroom])