from django.urls import path
from . import views

urlpatterns = [
    path('login/',         views.login_view,        name='login'),
    path('logout/',        views.logout_view,        name='logout'),
    path('register/',      views.register_view,      name='register'),
    path('profile-setup/', views.profile_setup_view, name='profile_setup'),
    path('edit-profile/',  views.edit_profile_view,  name='edit_profile'),
]
