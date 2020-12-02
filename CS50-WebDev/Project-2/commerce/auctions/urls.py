from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listings" , views.create_listing , name="create"),
    path("details/<str:name>" , views.listing_details , name="details"),
    path("watchlist/<str:name>" , views.add_watchlist , name="watchlist"),
    path("rm_watchlist/<str:name>" , views.remove_watchlist , name="rm_watchlist"),
    path("bids/<str:name>" , views.add_bid , name="bids"),
    path("close/<str:name>" , views.close_auction , name="close"),
]
