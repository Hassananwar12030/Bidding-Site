from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from commerce.settings import MEDIA_URL
from django.contrib.auth.decorators import login_required
from django import forms
from . models import User, list_item, bid, comment, watchlist

class listForm(forms.ModelForm):
    class Meta:
        model = list_item
        fields = ('title', 'bidPrice', 'category', 'picture_item', 'description')
        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'bidPrice': forms.NumberInput(attrs = {'class': 'form-control'}),
            'category': forms.Select(attrs = {'class': 'form-control'}),
            'picture_item': forms.FileInput(attrs = {'class': 'form-control-file'}),
            'description': forms.Textarea(attrs = {'class': 'form-control'}),
        }
def index(request):
    lists = list_item.objects.all()
    return render(request, "auctions/index.html", {"items": lists, "media_url":MEDIA_URL,})

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

def list_page(request, list_id):
    item = list_item.objects.get(id=list_id)
    if item.closed == False:
        comments_list = list(comment.objects.filter(item_id=item.id).values('comment', 'commenter'))
        comments= []
        for com in comments_list:
            entry = com.get('comment')
            comments.append(entry)
        if request.user.is_authenticated and (request.user).username == (item.item_creator).username:
           return render(request, "auctions/list_page.html",{
            "item": item,
            "media_url":MEDIA_URL,
            "comments": comments,
            "close_msg": "Close Bid"
            })
        else:
            if request.user.is_authenticated:
                try:
                    string = "Remove from WatchList"
                    obj = watchlist.objects.get(item_id=list_id, userName_id= request.user)
                    return render(request, "auctions/list_page.html",{
                        "item": item,
                        "media_url":MEDIA_URL,
                        "comments": comments,
                        "remove_list": string,
                    })
                except (watchlist.DoesNotExist):
                    return render(request, "auctions/list_page.html",{
                        "item": item,
                        "media_url":MEDIA_URL,
                        "comments": comments,
                    })
            else:
                return render(request, "auctions/list_page.html",{
                    "item": item,
                    "media_url":MEDIA_URL,
                    "comments": comments,
                })
    else:
        try:
            Bidder_obj = bid.objects.get(bid_id=item.id)
            Bidder = Bidder_obj.bidder
            Bidder_name = Bidder.username
            current_username = request.user.username
            if request.user.is_authenticated and Bidder_name == current_username:
                return render(request, "auctions/closed.html", {
                    "winner_msg": "Congratulations You have won the Bidding!"
                    })
            else:
                return render(request, "auctions/closed.html")
        except (bid.DoesNotExist):
            return render(request, "auctions/closed.html")

def list_bid(request, list_id):
    item = list_item.objects.get(id=list_id)
    comments_list = list(comment.objects.filter(item_id=item.id).values('comment', 'commenter'))
    if request.method == 'POST':
        if request.user.is_authenticated:
            request_bid = float(request.POST["bid"])
            current_bid = item.bidPrice
            comments= []
            for com in comments_list:
                entry = com.get('comment')
                comments.append(entry)
            if item.item_creator == request.user:
                return render(request, "auctions/list_page.html",{
                    "message": "Sorry. You can't bid because you are the creator of this page.",
                    "item": item,
                    "media_url":MEDIA_URL,
                    "comments": comments,
                    })
            else:
                if request_bid <= current_bid:
                    return render(request, "auctions/list_page.html",{
                        "message": "Please Place a bid greater than the existing Bid",
                        "item": item,
                        "media_url":MEDIA_URL,
                        "comments": comments,
                        })
                else:
                    item.bidPrice = request_bid
                    item.save()
                    new_bid = bid(bid_id=item.id, bidder= request.user)
                    new_bid.save()
                    return render(request, "auctions/list_page.html",{
                        "message": "Thank You for Placing the Bid",
                        "item": item,
                        "media_url":MEDIA_URL,
                        "comments": comments,
                        })
        else:
            return render(request, "auctions/login.html", {"message": "Please login first"})
    else:
        return HttpResponseRedirect(reverse('list_page', args=[list_id]))

def list_comment(request, list_id):
    item = list_item.objects.get(id=list_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            user_comment = request.POST["userComment"]
            new_comment = comment(item_id_id=item.id, commenter=request.user, comment=user_comment)
            new_comment.save()
            return HttpResponseRedirect(reverse('list_page', args=[list_id]))
            
        else:
            return render(request, "auctions/login.html", {"message": "Please login first"})
    else:
        return HttpResponseRedirect(reverse('list_page', args=[list_id]))


def create_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = listForm(request.POST, request.FILES)
            if form.is_valid():
                initiator = request.user
                title = form.cleaned_data["title"]
                bidPrice= request.POST["bidPrice"]
                category = request.POST["category"]
                description = request.POST["description"]
                image=request.FILES['picture_item']
                item = list_item(title=title, item_creator=initiator, bidPrice=bidPrice, category=category, picture_item= image, description= description)
                item.save()
                item_id = item.id
                return HttpResponseRedirect(f"list_page/{item_id}")
        else:
            form = listForm()
        return render(request, "auctions/create_page.html", {
            'form': form
        })

    else:
        return render(request, "auctions/login.html", {"message": "Please login first"})

def categories_display(request):
   categories = ["Fashion", "Toys", "Electronics", "Home", "Other"]
   return render(request, "auctions/categories.html", {"categories": categories})

def categories(request, category):
    items = list_item.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "items": items,
        "media_url":MEDIA_URL,
        "heading": category 
        })

def watchList(request, list_id):
    if request.user.is_authenticated:
        try:
            watchlist.objects.get(item_id=list_id, userName_id= request.user).delete()
            return HttpResponseRedirect(reverse('list_page', args=[list_id]))
        except (watchlist.DoesNotExist):
            add = watchlist(item_id=list_id, userName= request.user)
            add.save()
            return HttpResponseRedirect(reverse('list_page', args=[list_id]))
    else:
        return render(request, "auctions/login.html", {"message": "Please login first"})

def closedBid(request, list_id):
    item = list_item.objects.get(id=list_id)
    item.closed = True
    item.save()
    return render(request, "auctions/closed.html", {"success_msg": "Your Bid is successfully closed"})

def watchlist_display(request):
    list_dic = list(watchlist.objects.filter(userName_id=request.user).values('item'))
    items = []
    for item in list_dic:
        item_id = item.get('item')
        item_obj = list_item.objects.get(id=item_id)
        items.append(item_obj)

    return render(request, "auctions/watchlist_display.html", {"items": items})
