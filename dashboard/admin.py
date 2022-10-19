from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Account

class AccountInline(admin.TabularInline):
    model = Account

admin.site.register(User)
admin.site.register(Account)
