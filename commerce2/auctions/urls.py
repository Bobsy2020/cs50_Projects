from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('category/<str:category>/', views.filter_categories, name='filter_categories'),
    path('auctions/watchlist/<int:auction_id>/', views.watchlist, name='watchlist'),
    #path('balance/', views.balance, name='balance'),
    #path('balance/topup/', views.topup, name='topup'),
    #path('watchlist/', views.watchlist_page, name='watchlist'),
    #path('bid/<int:auction_id>/', views.bid_page, name='bid_page'),
    #path('bid/<int:auction_id>/comment/', views.comment, name='comment'),
    #path('bid/<int:auction_id>/raise_bid/', views.raise_bid, name='raise_bid'),
]
