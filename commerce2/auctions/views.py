from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Product, Watchlist
from itertools import chain


def index(request):
    """
    The main page of the website
    Returns
    -------
    HTTPResponse
        The index page with the current and future auctions.
    """
    # auctions = Auction.objects.filter(time_ending__gte=datetime.now()).order_by('time_starting')
    products = Product.objects.filter(active=True)

    try:
        if request.session['username']:
            # user = User.objects.get(username=request.session['username'])
            user = request.user

            w = Watchlist.objects.filter(user_id=user)
            # watchlist = Auction.objects.none()
            watchlist = Product.object.none()
            for item in w:
                # a = Auction.objects.filter(id=item.auction_id.id)
                a = Product.objects.filter(id = item.product)
                watchlist = list(chain(watchlist, a))

            # userDetails = UserDetails.objects.get(user_id=user.id)
            # return render(request, 'index.html',
                # {'auctions': auctions, 'balance': userDetails.balance, 'watchlist': watchlist})
            return render(request, 'auctions/index.html', {
                'products':products,
                'watchlist':watchlist
            })
    except KeyError:
        # return render(request, 'index.html', {'auctions': auctions})
        return render(request, 'auctions/index.html', {
            'products':products
        })

    # return render(request, 'index.html', {'auctions': auctions})
    return render(request, 'auctions/index.html', {
            'products':products
        })
   # return render(request, "auctions/index.html")


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

def watchlist(request, auction_id):
   return HttpResponse("TODO")
   # return index(request)

def watchlist_page(request):
   return HttpResponse("TODO")
   # return index(request)

def filter_categories(request, category):
   return HttpResponse("TODO")
   # return index(request)