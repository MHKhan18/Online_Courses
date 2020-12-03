from django.contrib import admin

from .models import User , Listings , Watchlist , Bid , Comments

admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Comments)
admin.site.register(Bid)