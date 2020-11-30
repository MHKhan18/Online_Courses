from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listings(models.Model):
    title = models.CharField(max_length=30 , unique=True)
    description = models.CharField(max_length=250)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images',blank=True, null=True)
    category = models.CharField(max_length=10)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f'title: {self.title} , bid: {self.bid} , owner: {self.owner.username} , image: {self.image} , category: {self.category}'


class Bid(models.Model):
    placed_bid = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "bids")
    listing = models.ForeignKey(Listings , on_delete=models.CASCADE , related_name="all_bids")
    
    def __str__(self):
        return f'customer: {self.customer.username}, product: {self.listing.title} , bid: {self.placed_bid}'

class Comments(models.Model):
    comment = models.CharField(max_length=1000)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "comments")
    listing = models.ForeignKey(Listings , on_delete=models.CASCADE , related_name="all_comments")

    def __str__(self):
        return f'customer: {self.customer.username}, product: {self.listing.title}, comment: {self.comment}'


class Watchlist(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listings , on_delete=models.CASCADE)

    def __str__(self):
        return f'customer: {self.customer.username}, product: {self.listing.title}'

    
