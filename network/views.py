from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Like, Follow


def index(request):
    posts = Post.objects.all()
    if request.method == "POST":
        if request.POST.get("post_contents"):
            p = Post(pk=request.POST.get("post_id"), poster=request.user)
            p.post = request.POST.get("post_contents")
            p.save()
            
        elif not request.POST.get("new_post"):
            return render(request, "network/index.html",{
                "posts": posts,
                "message": "Error: Blank posts are not allowed."
            })
        else:
            p = Post(poster=request.user, post=request.POST["post"])
            p.save()
    return render(request, "network/index.html", {
        "posts": posts
    })

def profile(request, user):
    if request.method == 'POST':
        if request.POST.get("post_contents"):
            p = Post(pk=request.POST.get("post_id"), poster=request.user)
            p.post = request.POST.get("post_contents")
            p.save()
    profile_user = User.objects.get(username=user)
    posts = Post.objects.filter(poster=profile_user)
    return render(request, "network/profile.html",{
        "posts": posts,
        "user": profile_user.username
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
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
        elif '' in [email,username,password,confirmation]:
            return render(request, "network/register.html", {
                "message": "All fields must be filled in."
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
