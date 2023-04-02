
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pg>", views.index, name="index_page"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("user-data/<str:user>", views.user, name="user-data"),
    path("likes/<int:post_id>", views.likes, name="post-likes"),
    path("following", views.following, name="following"),
]
