from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path('category/<str:category>/', views.filter_categories, name='filter_categories'),
    path('auctions/watchlist/<int:product_id>/<str:page>', views.watchlist, name='watchlist'),
    path('auctions/bids/<int:product_id>/', views.bids, name='bids'),
    #path('auctions/<int:product_id>/bids/', views.bids, name='bids'),
    #path("product/<int:pk>", views.product, name="product"),
    #path('balance/', views.balance, name='balance'),
    #path('balance/topup/', views.topup, name='topup'),
    path('watchlist_page/', views.watchlist_page, name='watchlist_page'),
    #path('bid/<int:auction_id>/', views.bid_page, name='bid_page'),
    #path('bid/<int:auction_id>/comment/', views.comment, name='comment'),
    #path('bid/<int:auction_id>/raise_bid/', views.raise_bid, name='raise_bid'),
]
