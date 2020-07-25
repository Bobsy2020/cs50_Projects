from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing
#from .models import Listing

from auctions.forms import ListingForm


def index(request):

    return render(request, "auctions/index.html", {
        'listings':Listing.objects.all()
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
def create(request):
    
    if request.method == "POST":
        #return HttpResponse("got to function")
        
        # Create a form instance and populate it with data from the request (binding):
        form = ListingForm(request.POST or None, request.FILES or None)

        # Check if the form is valid:
        if form.is_valid():
            
            lastimage= Listing.object.last()
            imagefile= lastimage.image

            form.instance.created_by = request.user
            form.save()

            return render(request, "auctions/create.html", {
                'form': form,
                'imagefile': imagefile
            })
            # redirect to a new URL:
            # return HttpResponseRedirect(reverse('index') )
            #return HttpResponse("TODO")
        # return HttpResponse(form)
    else:
        return render(request, "auctions/create.html", {
            'form':ListingForm
            
        })
     


