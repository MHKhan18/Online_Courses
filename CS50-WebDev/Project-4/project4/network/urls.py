
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("create", views.create_post, name="create"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("follow/<str:name>", views.follow, name="follow"),
    path("unfollow/<str:name>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),

    #API routes
    path("edit/<int:post_id>", views.edit, name="edit"),

]
