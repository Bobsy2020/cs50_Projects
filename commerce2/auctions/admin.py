from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import User, Product, Watchlist, Bids, Comments

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(Watchlist)
admin.site.register(Bids)
admin.site.register(Comments)
