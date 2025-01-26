from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_user, name='user_login'),
    path('logout/', views.logout_user, name='user_logout'),
    path('register/', views.register_user, name='register'),
    path("profile/", views.profile, name="profile"),
]