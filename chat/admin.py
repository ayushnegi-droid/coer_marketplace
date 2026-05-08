from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display  = ['sender', 'receiver', 'listing', 'timestamp']
    search_fields = ['sender__email', 'receiver__email', 'listing__title']
    ordering      = ['-timestamp']
