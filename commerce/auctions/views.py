from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid


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
        bid = Bid( 
            amount = price,
            n = 0
        )
        listing = Listing(
            lister=User.objects.get(username=request.user),
            title=request.POST["title"],
            description=request.POST["description"],
            image_URL=URL,
            bids = bid
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
        if request.POST.get("bid") and int(request.POST.get("bid")) >= listing.bids.amount:
            listing.bids.bidder = request.user
            listing.bids.amount = request.POST["bid"]
            listing.bids.n += 1
            listing.bids.save()
        elif request.POST.get("close"):
            listing.active = False
            listing.save()
        elif request.POST.get("watchlist") and not listing.is_watchlist:
            listing.is_watchlist = True
            listing.save()
        elif request.POST.get("watchlist") and listing.is_watchlist:
            listing.is_watchlist = False
            listing.save()
        return render(request, "auctions/listing.html", {
            'listing': Listing.objects.get(pk=id)
        }) 
    return render(request, "auctions/listing.html", {
        'listing': Listing.objects.get(pk=id)
    })


def error(request):
    return render(request, "auctions/error.html")


def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        'listings': Listing.objects.all()
    })