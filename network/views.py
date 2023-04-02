from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Post, Like, Follow


def index(request):
    posts = Post.objects.all().order_by('datetime')
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
            p = Post(poster=request.user, post=request.POST.get("new_post"))
            p.save()    
    return render(request, "network/index.html", {
        "posts": posts,
    })


@csrf_exempt
def profile(request, user):
    if request.method == 'POST':
        if request.POST.get("post_contents"):
            p = Post(pk=request.POST.get("post_id"), poster=request.user)
            p.post = request.POST.get("post_contents")
            p.save()
        elif request.body:
            follow = json.loads(request.body)
            if follow["follow"]:
                f = Follow(user=request.user, following_user=User.objects.get(username=user))
                f.save()
            elif not follow["follow"]:
                f = Follow.objects.get(user=request.user, following_user=User.objects.get(username=user))
                f.delete()
    profile_user = User.objects.get(username=user)
    posts = Post.objects.filter(poster=profile_user).order_by('datetime')
    followers = Follow.objects.filter(following_user=profile_user).count()
    following = Follow.objects.filter(user=profile_user).count()
    try:
        Follow.objects.get(user=request.user, following_user=User.objects.get(username=user))
        f_status = True
    except:
        f_status = False
    return render(request, "network/profile.html",{
        "posts": posts,
        "user": profile_user.username,
        "followers": followers,
        "following": following,
        "f_status": f_status
    })


@csrf_exempt
def likes(request, post_id):
    if request.method == "POST":
        like = json.loads(request.body)
        if like["liked"] == False:
            try:
                l = Like.objects.get(liker=request.user, status=True, post=Post.objects.get(pk=like["post_id"]))
                l.status = False
                l.save()
            except:
                l = Like.objects.filter(liker=request.user, status=True, post=Post.objects.get(pk=like["post_id"])).first()
                l.delete()
                l = Like.objects.get(liker=request.user, status=True, post=Post.objects.get(pk=like["post_id"]))
                l.status = False
                l.save()
        else:
            try:
                l = Like.objects.get(liker=request.user, status=False, post=Post.objects.get(pk=like["post_id"]))
                l.status = True
                l.save()
            except:
                l = Like.objects.create(liker=request.user, status=like["liked"], post=Post.objects.get(pk=like["post_id"]))
    try:
        post_liked = Like.objects.get(liker=request.user, post=Post.objects.get(pk=post_id)).status
    except:
        post_liked = False
    return JsonResponse({
        "post_id": post_id,
        "post_likes": Like.objects.filter(status=True, post=Post.objects.get(pk=post_id)).count(),
        "post_liked": post_liked,
    }, safe=False)


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


def user(_, user):
    profile_user = User.objects.get(username=user)
    return JsonResponse({
        "followers": Follow.objects.filter(following_user=profile_user).count(),
        "following": Follow.objects.filter(user=profile_user).count()
    }, safe=False)