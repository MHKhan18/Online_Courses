from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect , HttpResponseServerError , JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

from .models import User , Post , Profile , Like

import json


class NewPostForm(forms.Form):
    content = forms.CharField(label="" ,  max_length = 1000 , widget = forms.Textarea(attrs={'placeholder': 'Up to 1000 characters'}))

def index(request):
    posts_list = Post.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(posts_list , 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    user = request.user
    if user.is_authenticated:
        user_likes = user.likes.all()
        liked_posts = [like.post.id for like in user_likes]
    else:
        liked_posts = []


    return render(request, "network/index.html" , {
        "posts" : posts,
        "liked_posts" : liked_posts,
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
    posts_list = Post.objects.filter(author=user).all()

    page = request.GET.get('page', 1)

    paginator = Paginator(posts_list , 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

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

    user = request.user
    user_likes = user.likes.all()
    liked_posts = [like.post.id for like in user_likes]
        
    context = {
        "name" : name,
        "followers" : followers,
        "following" : following,
        "posts" : posts,
        "button" : button,
        "liked_posts" : liked_posts,
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
    posts_list = []
    
    friends = request.user.following.all()
    for friend in friends:
        cur_posts = Post.objects.filter(author = friend.user).all()
        posts_list += cur_posts

    page = request.GET.get('page', 1)
    paginator = Paginator(posts_list , 10)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    user = request.user
    user_likes = user.likes.all()
    liked_posts = [like.post.id for like in user_likes]


    return render(request, "network/index.html" , {
        "posts" : posts,
         "liked_posts" : liked_posts,
    })


@csrf_exempt
@login_required
def edit(request, post_id):
    
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@login_required
def like(request , post_id):

    
    user = request.user # can't get this in js!
    post = Post.objects.filter(id=post_id).first()

    to_like = False
    like = Like.objects.filter(user=user , post=post).first()
    if like:
        like.delete()
    else:
        to_like = True
        like = Like(user=user , post=post)
        like.save()

    response = {
        "post_id" : post_id,
        "to_like": to_like,
    }
    response = json.dumps(response)
    return HttpResponse(response, content_type = "application/json")

    


