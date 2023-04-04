from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json, datetime
from django.core.paginator import Paginator
from .models import User, Post, Like, Follow


def index(request, pg=1):
    if request.method == "POST":
        print('running this view')
        if not request.POST.get("new_post"):
            posts = []
            list = Post.objects.all().order_by('-datetime')
            for item in list:
                posts.append(item)
            page = Paginator(posts, 10)
            pages = range(1, page.num_pages+1)
            return render(request, "network/index.html",{
                "posts": page.page(pg),
                "message": "Error: Blank posts are not allowed.",
                "pages": pages,
                "current_page": pg,
                "previous_page": pg-1,
                "next_page": pg+1
            })
        else:
            p = Post(poster=request.user, post=request.POST.get("new_post"))
            p.save()
    posts = []
    list = Post.objects.all().order_by('-datetime')
    for item in list:
        posts.append(item)
    page = Paginator(posts, 10)
    pages = range(1, page.num_pages+1)
    print('about to render index')
    return render(request, "network/index.html", {
        "posts": page.get_page(pg),
        "pages": pages,
        "current_page": pg,
        "previous_page": pg-1,
        "next_page": pg+1
    })

@csrf_exempt
def profile(request, user, pg=1):
    if request.method == 'POST':
        print('this is running for some reason')
        if request.POST.get("post_contents"):
            p = Post(pk=request.POST.get("post_id"), poster=request.user)
            p.post = request.POST.get("post_contents")
            p.save()
        elif request.body:
            data = json.loads(request.body)
            if data["follow"]:
                f = Follow(user=request.user, following_user=User.objects.get(username=user))
                f.save()
            elif not data["follow"]:
                f = Follow.objects.get(user=request.user, following_user=User.objects.get(username=user))
                f.delete()
    profile_user = User.objects.get(username=user)
    posts = []
    list = Post.objects.filter(poster=profile_user).order_by('-datetime')
    for item in list:
        posts.append(item)
    page = Paginator(posts, 10)
    pages = range(1, page.num_pages+1)
    followers = Follow.objects.filter(following_user=profile_user).count()
    following = Follow.objects.filter(user=profile_user).count()
    try:
        Follow.objects.get(user=request.user, following_user=User.objects.get(username=user))
        f_status = True
    except:
        f_status = False
    return render(request, "network/profile.html",{
        "posts": page.page(pg),
        "user": profile_user.username,
        "followers": followers,
        "following": following,
        "f_status": f_status,
        "pages": pages,
        "current_page": pg,
        "previous_page": pg-1,
        "next_page": pg+1
    })


def following(request, pg=1):
    f = Follow.objects.filter(user=request.user)
    users = []
    for user in f:
        users.append(user.following_user.username)
    user_posts = User.objects.filter(username__in=users)
    posts = []
    list = Post.objects.filter(poster__in=user_posts).order_by('-datetime')
    for item in list:
        posts.append(item)
    page = Paginator(list, 10)
    pages = range(1, page.num_pages+1)
    return render(request, "network/following.html", {
        "posts": page.page(pg),
        "pages": pages,
        "current_page": pg,
        "previous_page": pg-1,
        "next_page": pg+1
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
                Like.objects.create(liker=request.user, status=True, post=Post.objects.get(pk=like["post_id"]))
                while Like.objects.filter(liker=request.user, status=True, post=Post.objects.get(pk=like["post_id"])).count() > 1:
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
    if request.user.is_authenticated:
        try:
            post_liked = Like.objects.get(liker=request.user, post=Post.objects.get(pk=post_id)).status
        except:
            l = Like.objects.create(liker=request.user, status=False, post=Post.objects.get(pk=post_id))
            post_liked = l.status
    
        # Prevents multiple like objects with a user being associated with a post
        while Like.objects.filter(liker=request.user, post=Post.objects.get(pk=post_id)).count() > 1:
            print('its deletin time')
            l = Like.objects.filter(liker=request.user, post=Post.objects.get(pk=post_id)).first()
            l.delete()
    else:
        post_liked = None

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


def post(request, post_id): 
    if request.method == "POST":
        user_post = json.loads(request.body)   
        p = Post.objects.get(pk=user_post["post_id"])
        p.post = user_post["post"]
        p.save()
        return HttpResponse('')
    elif request.method == "GET":
        return JsonResponse({
            "post": Post.objects.get(pk=post_id).post,
            "post_id": post_id,
        }, safe=False)