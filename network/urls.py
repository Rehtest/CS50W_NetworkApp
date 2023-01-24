
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user_view>", views.user_page, name="profile"),
    path("following", views.following, name="following"),

    #API lRoutes
    path("save", views.save, name="save"),
    path("like", views.like, name="like")
]
