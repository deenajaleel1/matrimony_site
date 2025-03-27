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
    path('profile/<int:id>/', views.profile_detail, name='profile_detail'),
    path('matches/', views.matches, name='matches'),
    path('search_matches/', views.search_matches, name='search_matches'),
    path('chat_view/<int:receiver_id>/',views.chat_view,name="chat_view"),
    path('send_message/<int:receiver_id>/',views.send_message, name='send_message'),
    path('recent_chats/',views.recent_chats,name="recent_chats"),
    path('search_users/',views.search_users,name="search_users"),
    path('logout/', views.user_logout, name='logout'),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
]

# Serve media files only in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)