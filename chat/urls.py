from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$',  views.home, name='home'),
    url(r'^accounts/login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^available_chats/$', views.available_chats, name='available_chats'),
    url(r'^(?P<username>[\w-]{,50})/$', views.chat_room, name='chat_room'),
]
