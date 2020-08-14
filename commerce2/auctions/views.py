from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Product, Watchlist, Bids, Category
from auctions.forms import ProductForm, CommentForm
from itertools import chain
from auctions.templatetags.custom_tags import current_price
import locale



def index(request):
    """
    The main page of the website
    Returns
    -------
    HTTPResponse
        The index page with the current and future auctions.
    """
    user = request.user.id
    
    products = Product.objects.filter(active=True)
    watchlist = Watchlist.objects.filter(user_id=user)

    return render(request, 'auctions/index.html', {
                'page_title':'Active Listings',
                'products':products,
                'watchlist':watchlist
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
def watchlist(request, product_id, page):
    user = request.user.id
    w = Watchlist.objects.filter(product_id=product_id).filter(user_id=user)
    if not w:
        watchlist_item = Watchlist(
        product_id = product_id,
        user_id = user
        )
        watchlist_item.save()
        
    else:
        w.delete()
    # return the to the page that the function was called from
    if page == "bids":
        return HttpResponseRedirect(reverse('bids', args=(product_id,)))
    return HttpResponseRedirect(reverse(page))
    


def watchlist_page(request):
    #return HttpResponse("TODO")
    #user = request.user.id
    

    try:
        
            #return HttpResponse("TODO")
            # user = User.objects.filter(username=request.session['username'])
            user = request.user.id
            
            w = Watchlist.objects.filter(user_id=user)
            
            products = Product.objects.none()
            for item in w:
                p = Product.objects.filter(id=item.product.id).filter(active=True)
                
                products = list(chain(products, p))
            # return HttpResponse(products)
            return render(request, 'auctions/index.html', {
                'page_title':'Watchlist',
                'products': products,
                #'user': user[0],
                'watchlist':w
            })
    except KeyError:
        return HttpResponseRedirect(reverse('index'))

def filter_categories(request, category):
    user = request.user.id
    
    products = Product.objects.filter(active=True).filter(category=category)
    watchlist = Watchlist.objects.filter(user_id=user)
    
    #category_name = Category.objects.filter(id=category)
    categories = Category.objects.values_list("category", flat=True).get(id=category)
    #return HttpResponse(categories)
    pagetitle = f"Active Listings for Category : {categories}"

    return render(request, 'auctions/index.html', {
                'page_title':pagetitle,
                'products':products,
                'watchlist':watchlist
            })

    
   # return index(request)

@login_required
def create(request):
    
    if request.method == "POST":
        # Create a form instance and populate it with data from the request (binding):
        form = ProductForm(request.POST or None, request.FILES or None)

        # Check if the form is valid:
        if form.is_valid():
            
            form.instance.created_by = request.user
            form.save()

            return render(request, "auctions/create.html", {
                'form': form,
            })
    else:
        return render(request, "auctions/create.html", {
            'form':ProductForm
            
        })

@login_required
def bids(request, product_id, method="POST"):
    currency_symbol = locale.currency(0.0)
    currency_symbol = str(currency_symbol).replace("0.00", "")
    
    # return HttpResponse(currency_symbol)
    if request.method=="POST":
        bid_price = request.POST.get("bid_price")
        bid_by = request.user
        # create an instance of the Product object
        product = Product.objects.get(id=product_id)
        product_price = locale.atof(current_price(product.id)[1:])
        

        # check to see if the bid is valid (ie. > than the current max)
        # if there is nothing entered then display an error banner
        if len(bid_price) == 0:
            message = "You must enter a bid value."
            alert = "alert alert-warning"
        # if the current price is greater that the bid price then 
        # display an error message
        elif float(product_price) > float(bid_price):
            message = "Amount bid must be more than the current price."
            alert = "alert alert-warning"
        else:
            # add the record to the Bids table
            if Bids.objects.filter(product=product_id):
                Bids.objects.filter(product=product_id).update(
                    user=bid_by,
                    amount_bid=bid_price,
                    number_of_bids = F('number_of_bids') + 1
                )
            else:
                b = Bids(
                    product = product,
                    user=bid_by,
                    amount_bid=bid_price,
                )
                b.save()
            
            message = "Bid accepted"
            alert = "alert alert-success"
            # return redirect('/listing/'+str(pk))
            # return redirect('listing', pk=pk)
            return HttpResponseRedirect(reverse('bids', args=(product_id,)))
        return render(request, "auctions/bids.html", {
            'message': message,
            'alert': alert,
            'product':product,
            'currency':currency_symbol
            
        })
        # return HttpResponse("TODO")
    else:
        product = Product.objects.get(id=product_id)
        watchlist = Watchlist.objects.filter(user_id=request.user)
        comments = product.comments.all().order_by('-created')
        

        return render(request, "auctions/bids.html", { 
            'product':product,
            'watchlist':watchlist,
            'currency':currency_symbol,
            'comments':comments
       })


def close(request, product_id):
    # product_id = self.kwargs.get('product_id')
    Product.objects.filter(id=product_id).update(
                    active=False
                )
    return HttpResponseRedirect(reverse('index'))

@login_required
def comments(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == "POST":
        # Create a form instance and populate it with data from the request (binding):
        form = CommentForm(request.POST or None)

        # Check if the form is valid:
        if form.is_valid():
            form.instance.product = product
            form.instance.user = request.user
            form.save()

            return HttpResponseRedirect(reverse('bids', args=(product_id,)))
            #return render(request, "auctions/bids {{ product.id }}.html", {
            #    'form': form,
            #})
    else:
        #return HttpResponseRedirect(reverse('bids', args=(product_id,)))
        return render(request, "auctions/comments.html", {
            'product':product,
            'form':CommentForm
            
        })    


    