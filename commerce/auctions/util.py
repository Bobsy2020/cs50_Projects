import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import User, Listing, category, Bids
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect

def maxval(pk):

    """ Finds the max price bid or the list price in there are no bids 
    bases on the Listin ID"""
    
    mp = Bids.objects.filter(listing = pk)
    if mp:
        maxval=mp.aggregate(maxval=Max('bid_price'))['maxval']
    else:
        #maxval=Listing.objects.filter(id=pk).price
        maxval=Listing.objects.values_list('price', flat=True).get(id=pk)
    return round(float(maxval),2)