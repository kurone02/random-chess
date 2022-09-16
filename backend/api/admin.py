from django.contrib import admin
from .form import MyUserAdmin
from .models import User, Match

admin.site.register(User, MyUserAdmin)
admin.site.register(Match)
