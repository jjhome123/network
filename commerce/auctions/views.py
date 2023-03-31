from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Watchlist, Comment


def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all()
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


@login_required
def create_listing(request):
    if request.method == 'POST':
        if request.POST["image_URL"] == '' or 'https://' not in request.POST["image_URL"]:
            URL = 'https://www.caltrain.com/files/images/2021-09/default.jpg'
        else:
            URL = request.POST["image_URL"]
        if not request.POST["price"]:
            price = 0
        else:
            price = request.POST["price"]
        if request.POST["title"] == '':
            title = 'Untitled'
        else:
            title=request.POST["title"]
        if request.POST["description"] == '':
            description = 'No description for this listing.'
        else:
            description = request.POST["description"]
        bid = Bid(amount=price,n=0)
        listing = Listing(
            lister=User.objects.get(username=request.user),
            title=title,
            description=description,
            image_URL=URL,
            bids=bid,
            watchlist=None,
            category=request.POST["category"]
        )
        bid.save()
        listing.save()
        return HttpResponseRedirect(reverse('index'))
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "auctions/create_listing.html")


def listing(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        c = Comment.objects.filter(item=listing)
        try:
            w = Watchlist.objects.get(watcher=request.user, item=Listing.objects.get(pk=id))
        except:
            w = None
        if request.POST.get("bid") and float(request.POST.get("bid")) >= listing.bids.amount:
            listing.bids.bidder = request.user
            listing.bids.amount = request.POST["bid"]
            listing.bids.n += 1
            listing.bids.save()
        elif request.POST.get("close"):
            listing.active = False
            listing.save()
        elif request.POST.get("add_watchlist"):
            try: 
                w = Watchlist.objects.get(watcher=request.user, item=listing, is_watchlist=False)
                w.is_watchlist = True
                w.save()
            except:
                w = Watchlist(watcher=request.user, item=listing, is_watchlist=True)
                w.save()    
        elif request.POST.get("remove_watchlist"):
            w = Watchlist.objects.get(watcher=request.user, item=listing, is_watchlist=True)
            w.is_watchlist = False
            w.delete()
        elif request.POST.get("add_comment"):
            c = Comment(commenter=request.user, item=listing, comment=request.POST.get("add_comment"))
            c.save()
        return render(request, "auctions/listing.html", {
            'listing': Listing.objects.get(pk=id),
            'watchlist': w,
            'comments': Comment.objects.filter(item=Listing.objects.get(pk=id))
        }) 
    c = Comment.objects.filter(item=Listing.objects.get(pk=id))
    try:
        w = Watchlist.objects.get(watcher=request.user, item=Listing.objects.get(pk=id))
    except:
        w = None
    return render(request, "auctions/listing.html", {
        'listing': Listing.objects.get(pk=id),
        'watchlist': w,
        'comments': c
    })


def error(request):
    return render(request, "auctions/error.html")


def categories(request):
    l = Listing.objects.all()
    categories = []
    for listing in l:
        categories.append(listing.category)
    categories=set(categories)
    return render(request, "auctions/categories.html", {
        'categories': categories
    })


def c_listings(request, category):
    l = Listing.objects.filter(category=category)
    return render(request, "auctions/c_listings.html", {
        'listings': l
    })


def watchlist(request):
    Watchlist.objects.filter(watcher=request.user)
    return render(request, "auctions/watchlist.html", {
        'watchlist': Watchlist.objects.filter(watcher=request.user)
    })

