from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django import forms
from django.contrib.auth.decorators import login_required

from .models import User , Listings




CATEGORY_CHOICES = [
    ('None' , ''),
    ('Fashion' , 'Fashion'),
    ('Toys' , 'Toys'),
    ('Electronics' , 'Electronics'),
    ('Home' , 'Home'),
    ('Car' , 'Car'),
    ('Airplane' , 'Airplane')
]

class CreateListingsFrom(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description" , widget = forms.Textarea)
    bid = forms.DecimalField(label="Starting Bid" , decimal_places=2)
    image = forms.ImageField(label="Upload an image(optional)" , required=False)
    category = forms.CharField(label="Category (optional):",  required=False , widget = forms.Select(choices = CATEGORY_CHOICES))




def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/login')
def create_listing(request):

    if request.method == "POST":
        form = CreateListingsFrom(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data['description']
            bid = form.cleaned_data['bid']
            image = form.cleaned_data['image']
            category = form.cleaned_data['category']
            owner = request.user 
            try:
                listing = Listings(title=title , description=description , bid=bid , image=image , category=category , owner=owner)
                listing.save()
                return HttpResponseRedirect(reverse("index"))
            except IntegrityError:
                return render(request , "auctions/create_listings.html" , {"form" : form , "error" : "Listing with this title already exists."}) 


        return render(request , "auctions/create_listings.html" , {"form" : form}) # display errors

    else:
        form = CreateListingsFrom()
        return render(request , "auctions/create_listings.html" , {"form" : form})
