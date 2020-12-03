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
    path("comment/<str:name>" , views.add_comment , name="comment"),
    path("get-watchlist" , views.get_watchlist , name="get_watchlist"),
    path("get-categories" , views.get_categories , name="get_categories"),
    path("cat-items/<str:name>" , views.cat_items , name="cat_items"),
]
