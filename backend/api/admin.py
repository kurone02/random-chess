from django.contrib import admin
from .models import User, Match

admin.site.register([User, Match])
