from django.urls import path
from . import views

urlpatterns = [
    path('<int:listing_id>/', views.chat_view, name='chat'),
    path('<int:listing_id>/<int:buyer_id>/', views.chat_view, name='chat_with_buyer'),
]