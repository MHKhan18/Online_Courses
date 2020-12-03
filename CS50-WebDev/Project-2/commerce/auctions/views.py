from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect , HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from django import forms
from django.contrib.auth.decorators import login_required

from .models import User , Listings , Watchlist , Bid , Comments
from django.db.models import Max



CATEGORY_CHOICES = [
    ('None' , ''),
    ('Fashion' , 'Fashion'),
    ('Toys' , 'Toys'),
    ('Electronics' , 'Electronics'),
    ('Home' , 'Home'),
    ('Car' , 'Car'),
    ('Airplane' , 'Airplane'),
    ('Book' , 'Book'),
]

class CreateListingsForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description" , widget = forms.Textarea)
    bid = forms.DecimalField(label="Starting Bid" , max_digits=10 , decimal_places=2)
    image = forms.ImageField(label="Upload an image(optional)" , required=False)
    category = forms.CharField(label="Category (optional):",  required=False , widget = forms.Select(choices = CATEGORY_CHOICES))

class BidForm(forms.Form):
    bid = forms.DecimalField(decimal_places=2 , widget=forms.TextInput(attrs={'placeholder': 'Bid'}))

class CommentForm(forms.Form):
    comment = forms.CharField(label="Comment:", max_length = 1000 , widget = forms.Textarea(attrs={'placeholder': 'Up to 1000 characters'}))


def index(request):
    listings = Listings.objects.all()
    return render(request, "auctions/index.html" , {"listings" : listings})


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
        form = CreateListingsForm(request.POST, request.FILES)
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
            else:
                return render(request , "auctions/create_listings.html" , {"form" : form , "error" : "Description can have maximum 250 characters and bid can be at most 10 digits."})


        return render(request , "auctions/create_listings.html" , {"form" : form}) # display errors

    else:
        form = CreateListingsForm()
        return render(request , "auctions/create_listings.html" , {"form" : form})


def listing_details(request , name:str):
    
    listing = Listings.objects.filter(title=name).first()
    form = BidForm()
    comment_form = CommentForm()

    watchlist = Watchlist.objects.filter(customer__username = request.user.username , listing__title = listing.title).first()
    can_watchlist = True if watchlist == None else False

    prev_bids = listing.all_bids.all()
    num_bids = prev_bids.count()
    status = "No bid yet, be the first!"
    if num_bids > 0:
        prev_max = prev_bids.aggregate(Max('placed_bid'))["placed_bid__max"]
        status = f"{num_bids} bid(s) so far, going at ${prev_max}"

    comments = listing.all_comments.all()

    return render(request , "auctions/details.html", 
    {"listing" : listing , "form" : form , "can_watchlist" : can_watchlist , "status" : status , 
    "num_bids" : num_bids , "comment_form" : comment_form , "comments" : comments})
    
@login_required(login_url='/login')
def add_watchlist(request , name:str):
    
    listing = Listings.objects.filter(title=name).first()
    watch_item = Watchlist(customer = request.user , listing = listing)
    watch_item.save()

    return HttpResponseRedirect(reverse("details", args=(name,)))

@login_required(login_url='/login')
def remove_watchlist(request , name:str):
    
    listing = Listings.objects.filter(title=name).first()
    watch_item =  Watchlist.objects.filter(customer__username = request.user.username , listing__title = listing.title)
    watch_item.delete()
    
    return HttpResponseRedirect(reverse("details", args=(name,)))

@login_required(login_url='/login')
def add_bid(request , name:str):

    listing = Listings.objects.filter(title=name).first()
    form = BidForm()
    comment_form = CommentForm()

    watchlist = Watchlist.objects.filter(customer__username = request.user.username , listing__title = listing.title).first()
    can_watchlist = True if watchlist == None else False

    comments = listing.all_comments.all()

    if request.method == "POST":
        
        bid_form = BidForm(request.POST)
        
        if bid_form.is_valid():
            
            new_bid = float(bid_form.cleaned_data["bid"])

            prev_bids = listing.all_bids.all()
            num_bids = prev_bids.count()

            prev_max = float('-inf')
            if num_bids > 0:
                prev_max = prev_bids.aggregate(Max('placed_bid'))["placed_bid__max"]
                
            if (num_bids == 0 and new_bid < listing.bid) or new_bid <= prev_max:
                status = "Error: Only bids that are greater than current going rate are accepted."
            else:
                bid_added = Bid(placed_bid = new_bid , customer = request.user , listing = listing)
                bid_added.save()
                status = f"{num_bids+1} bid(s) so far. Your bid (${new_bid}) is the current bid."

            return render(request , "auctions/details.html", {"listing" : listing , "form" : form , "can_watchlist" : can_watchlist , 
                            "status" : status , "num_bids" : num_bids , "comment_form" : comment_form ,"comments" : comments})



        else:
            status = "Error: Please enter valid bid."
            return render(request , "auctions/details.html", {"listing" : listing , "form" : bid_form , "can_watchlist" : can_watchlist , 
                        "status" : status, "num_bids" : num_bids , "comment_form" : comment_form ,"comments" : comments})


@login_required(login_url='/login')
def close_auction(request , name:str):
    listing = Listings.objects.filter(title=name).first()
    bids = listing.all_bids.all()
    max_bid = bids.aggregate(Max('placed_bid'))["placed_bid__max"]
    win_bid = Bid.objects.filter(listing__title = name , placed_bid = max_bid).first()
    listing.is_won = True
    listing.save()
    listing.winner = win_bid.customer
    listing.save()
    listing.win_price = max_bid
    listing.save()
    return HttpResponseRedirect(reverse("details", args=(name,)))

@login_required(login_url='/login')
def add_comment(request , name:str):
    
    listing = Listings.objects.filter(title=name).first()
    
    form = BidForm()
    input_form = CommentForm()
    
    watchlist = Watchlist.objects.filter(customer__username = request.user.username , listing__title = listing.title).first()
    can_watchlist = True if watchlist == None else False

    prev_bids = listing.all_bids.all()
    num_bids = prev_bids.count()
    status = "No bid yet, be the first!"
    if num_bids > 0:
        prev_max = prev_bids.aggregate(Max('placed_bid'))["placed_bid__max"]
        status = f"{num_bids} bid(s) so far, going at ${prev_max}"
    
    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            user_comment = comment_form.cleaned_data["comment"]
            comment_item = Comments(comment = user_comment , customer = request.user , listing = listing)
            comment_item.save()

            comments = listing.all_comments.all()
            return render(request , "auctions/details.html", {"listing" : listing , "form" : form , "can_watchlist" : can_watchlist , 
                          "status" : status , "num_bids" : num_bids , "comment_form" : input_form ,"comments" : comments})
        
        else:
            return render(request , "auctions/details.html", {"listing" : listing , "form" : form , "can_watchlist" : can_watchlist , 
                        "status" : status , "num_bids" : num_bids , "comment_form" : comment_form ,"comments" : comments})
            