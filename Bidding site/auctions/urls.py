from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("list_page/<int:list_id>", views.list_page, name="list_page"),
    path("create_page", views.create_page, name="create_page"),
    path("list_page/comment/<int:list_id>", views.list_comment, name="list_comment"),
    path("list_bid/<int:list_id>", views.list_bid, name="list_bid"),
    path("categories_display", views.categories_display, name="categories_display"),
    path("categories/<str:category>", views.categories, name="categories"),
    path("watchList/<int:list_id>", views.watchList, name="watchList"),
    path("closedBid/<int:list_id>", views.closedBid, name="closedBid"),
    path("watchlist_display", views.watchlist_display, name="watchlist_display")

]
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)