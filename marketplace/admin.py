from django.contrib import admin
from .models import Listing, Wishlist


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display   = ['title', 'seller', 'price', 'category', 'status', 'created_at']
    list_filter    = ['category', 'status']
    search_fields  = ['title', 'seller__email']
    ordering       = ['-created_at']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display  = ['user', 'listing', 'added']
    search_fields = ['user__email', 'listing__title']
