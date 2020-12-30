from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect , HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import User , Post , Profile


class NewPostForm(forms.Form):
    content = forms.CharField(label="" ,  max_length = 1000 , widget = forms.Textarea(attrs={'placeholder': 'Up to 1000 characters'}))

def index(request):
    posts = Post.objects.all()
    return render(request, "network/index.html" , {
        "posts" : posts,
    })


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        # Ensure password matches confirmation
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='/login')
def create_post(request):
   
    if request.method == "POST":
        form = NewPostForm(request.POST)
        
        if form.is_valid():
            author = request.user
            content = form.cleaned_data['content']
            try:
                post = Post(author=author , content=content)
                post.save()
                
            except Exception as e:
                print(str(e))
                return HttpResponseServerError()
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request , "network/create.html" , {
            "form" : NewPostForm()
        })

@login_required(login_url='/login')
def profile(request , name):

    profile = Profile.objects.filter(user__username=name).first()
    followers = profile.followers.count()
    user = profile.user
    following = user.following.count()
    posts = Post.objects.filter(author=user).all()

    if name == request.user.username:
        button = None
    else:
        client = request.user.username
        is_following = False
        for follower in profile.followers.all():
            if follower.username == client:
                is_following = True 
        if is_following:
            button = "Unfollow"
        else:
            button = "Follow"

        
    context = {
        "name" : name,
        "followers" : followers,
        "following" : following,
        "posts" : posts,
        "button" : button,
    }
    return render(request , "network/profile.html" , context)


@login_required(login_url='/login')
def follow(request , name):
    user = request.user
    profile = Profile.objects.filter(user__username=name).first()
    profile.followers.add(user)
    return HttpResponseRedirect(reverse("profile", args=(name,)))



@login_required(login_url='/login')
def unfollow(request , name):
    user = request.user
    profile = Profile.objects.filter(user__username=name).first()
    profile.followers.remove(user)
    return HttpResponseRedirect(reverse("profile", args=(name,)))

@login_required(login_url='/login')
def following(request):
    posts = []
    
    friends = request.user.following.all()
    for friend in friends:
        cur_posts = Post.objects.filter(author = friend.user).all()
        posts += cur_posts

    return render(request, "network/index.html" , {
        "posts" : posts,
    })

    


    