from django.urls import path
from . import views

urlpatterns = [
    path('',                      views.home_view,       name='home'),
    path('sell/',                  views.sell_view,       name='sell'),
    path('item/<int:pk>/',         views.detail_view,     name='detail'),
    path('dashboard/',             views.dashboard_view,  name='dashboard'),
    path('wishlist/<int:pk>/',     views.toggle_wishlist, name='toggle_wishlist'),
    path('sold/<int:pk>/',         views.mark_sold,       name='mark_sold'),
    path('available/<int:pk>/',    views.mark_available,  name='mark_available'),
    path('delete/<int:pk>/',       views.delete_listing,  name='delete_listing'),
]
