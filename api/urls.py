from django.contrib import admin
from django.urls import path

from .views import LoginView, LogoutView, ProfileView, RegisterUserView

urlpatterns = [
    path('signup/', RegisterUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', ProfileView.as_view()),
]