from django import template
from ..models import User
from django.utils import timezone
from django.http import HttpResponse

register = template.Library()

@register.filter(name='search')
def search(value, id):
    # return HttpResponse("got here")
    for v in value:
        if v.product == id:
            return True
    return False

@register.filter(name="current_price")
def current_price(value):
    # current_cost = 0.20 + (value.number_of_bids * 0.20)
    # current_cost = "%0.2f" % current_cost
    current_cost = 100 * 0.5
    return current_cost

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