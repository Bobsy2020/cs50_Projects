from django.contrib.auth.models import AbstractUser
from django.db import models
import locale
locale.setlocale(locale.LC_ALL, '')

class User(AbstractUser):
    pass

class Product(models.Model):
    CATEGORIES = (
		('LAP', 'Laptop'),
		('CON', 'Console'),
		('GAD', 'Gadget'),
		('GAM', 'Game'),
		('TEL', 'TV')
	)
    title= models.CharField(max_length=60)
    description = models.TextField(max_length=256)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    price_currency = models.CharField(max_length=60, null=True, blank=True, default=locale.getdefaultlocale(locale.LC_MONETARY))
    image= models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Upload image")
    # category = models.ForeignKey(category, null=True, blank=True, on_delete=models.CASCADE, related_name='+')
    category = models.CharField(
		max_length=3,
		choices=CATEGORIES
	)
    active = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,editable=False,null=True,blank=True, on_delete=models.CASCADE)
    objects = models.Manager()
    # def current_price(self):
    #    "Returns the current price"
    #    mp = Bids.objects.filter(listing = self.pk)
    #    if mp:
    #        maxval=mp.aggregate(maxval=Max('bid_price'))['maxval']
    #    else:
    #        maxval=self.price
    #    maxval = locale.currency(maxval, grouping=True)
    #    return maxval

    def __str__(self):
        #return f"{self.title}: {self.description} @ {self.price}"
        return "ID:" + str(self.pk) + " " + self.title

class Watchlist(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # objects = models.Manager()
	
	def __str__(self):
		return "USER_ID:" + str(self.user) + " PRODUCT_ID:" + str(self.product)

class Bids(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_bid = models.DecimalField(max_digits=7, decimal_places=2)
    number_of_bids = models.IntegerField()
    
    def __str__(self):
	    return "USER_ID:" + str(self.user) + " PRODUCT_ID:" + str(self.product) + " AMOUNT_BID:" + str(self.amount_bid)