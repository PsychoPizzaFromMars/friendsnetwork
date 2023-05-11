from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path("register/", RegisterUserView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("profile/friends/", FriendsListView.as_view()),
    path("profile/friendships/", FriendshipsListView.as_view()),
    path("profile/friendships/<int:to_user_id>", FriendshipView.as_view()),
]
