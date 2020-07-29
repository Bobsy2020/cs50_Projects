
from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField
from django.db.models import Max
import decimal
import locale
locale.setlocale(locale.LC_ALL, '')

class User(AbstractUser):
    pass


class category(models.Model):
    category = models.CharField(max_length=60)

    def __str__(self):
        return self.category

class Listing(models.Model):
    title= models.CharField(max_length=60)
    description = models.TextField(max_length=256)
    #price = MoneyField(max_digits=7, decimal_places=2, default_currency='USD')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    price_currency = models.CharField(max_length=3, null=True, blank=True, default=locale.getdefaultlocale(locale.LC_MONETARY))
    image= models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Upload image")
    category = models.ForeignKey(category, null=True, blank=True, on_delete=models.CASCADE, related_name='+')
    active = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,editable=False,null=True,blank=True, on_delete=models.CASCADE)
    def current_price(self):
        "Returns the current price"
        mp = Bids.objects.filter(listing = self.pk)
        if mp:
            maxval=mp.aggregate(maxval=Max('bid_price'))['maxval']
        else:
            maxval=self.price
        #maxval = '{:f}'.format(maxval)
        maxval = locale.currency(maxval, grouping=True)
        return maxval



    #        import datetime
    #        if self.birth_date < datetime.date(1945, 8, 1):
    #            return "Pre-boomer"
    #elif self.birth_date < datetime.date(1965, 1, 1):
    #    return "Baby boomer"
    #else:
    #    return "Post-boomer"

  #def _get_full_name(self):
  #  "Returns the person's full name."
  #  return '%s %s' % (self.first_name, self.last_name)
  #full_name = property(_get_full_name)





    objects = models.Manager()

    def __str__(self):
        #return self.title
        return f"{self.title}: {self.description} @ {self.price}"


class Bids(models.Model):
    listing = models.ForeignKey(Listing,  on_delete=models.CASCADE, related_name='+')
    bid_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='+')
    #bid_price = MoneyField(max_digits=7, decimal_places=2, default_currency='USD')
    bid_price = models.DecimalField(max_digits=7, decimal_places=2)
    bid_price_currency = models.CharField(max_length=3, 
        null=True, 
        blank=True, 
        default=locale.getdefaultlocale(locale.LC_MONETARY)
        )
    bid_time = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.bid_price