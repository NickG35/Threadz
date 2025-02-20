from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_user, name='user_login'),
    path('logout/', views.logout_user, name='user_logout'),
    path('register/', views.register_user, name='register'),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("profile/<int:profile_id>/update_password/", views.update_password, name='update_password'),
    path("profile/<int:profile_id>/update_user/", views.update_user, name='update_user')
]