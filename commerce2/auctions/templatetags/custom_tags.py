from django import template
from ..models import User, Bids, Product, Watchlist
import locale

from django.utils import timezone
from django.http import HttpResponse

register = template.Library()

locale.setlocale(locale.LC_ALL, '')

@register.filter(name='search')
def search(value, id):
    # return HttpResponse("got here")
    for v in value:
        if v.product == id:
            return True
    return False

@register.filter(name="current_price")
def current_price(id):
    mp = Bids.objects.filter(product = id)
    
    if mp:
        #price=mp.amount_bid
        price=Bids.objects.values_list('amount_bid', flat=True).get(product_id = id)
    else:
        price=Product.objects.values_list('price', flat=True).get(id=id)
    current_cost =  locale.currency(price, grouping=True)
    return current_cost

@register.filter(name="watchlist_count")
def watchlist_count(id):
    watchlist_count = Watchlist.objects.filter(user=id).count()
    return watchlist_count



@register.filter(name="time_left")
def time_left(value):
    """
    Calculates the remaining time by
    subtracting the deadline with the 
    current time and converts it to 
    string with {minutes}m {seconds}s
    format. 
    Parameters
    ----------
    value : DateTime
        The deadline
    
    Returns
    ------
    string
        Remaining time in minutes and seconds
    """
    t = value - timezone.now()
    days, seconds = t.days, t.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    st = str(minutes) + "m " + str(seconds) + "s"
    return st 