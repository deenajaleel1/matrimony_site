# matrimony_app/urls.py
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.matrimony_home, name='home'),
    path('login/', views.login_view, name='login'), 
    path('registration/', views.registration_view, name='registration'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("edit_preferences/", views.edit_preferences, name="edit_preferences"),
]

# Serve media files only in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)