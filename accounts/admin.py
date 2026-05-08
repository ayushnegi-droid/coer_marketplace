from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display  = ['email', 'username', 'is_active', 'date_joined']
    ordering      = ['-date_joined']
    search_fields = ['email']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display  = ['full_name', 'user', 'department', 'year', 'setup_done']
    search_fields = ['full_name', 'user__email']
