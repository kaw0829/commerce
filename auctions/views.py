from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext as _
from django.conf import settings
from . models import User, Listing, Listing_Comment, Bid

#model objects.filter will filter for only a certain result listing.filter(listing_cat == HOME)
# ModelForm takes a model and creates a form,  has a .save method to save to post data to db.
class BidsForm(forms.Form):
    placed_bid = forms.DecimalField(label='bid', decimal_places=2)
   

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['username', 'amount_bid', 'listing_id']
        labels = {
            'username': _('Name'),
        }
   

class AddListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["listing_cat", "listing_name","description","starting_bid", "close_date", "listing_img"]
        labels = {
            'listing_name': _('Name'),
            'listing_cat': _('Category'),
            "listing_img": _("Pictures")
        }
        # help_texts = {
        #     'listing_name': _('name of item'),
        # }
        error_messages = {
            'description': {
                'max_length': _("This description is too long."),
            }},
        # widgets = {
        #     'description': Textarea(attrs={'cols': 4, 'rows': 10}),
        # }

# Active Listings Page: The default route of your web application should let users view all of the currently
#  active auction listings. For each active listing, this page should display (at minimum) the title, 
#  description, current price, and photo (if one exists for the listing).

def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.listings.all(),
        'media_url': settings.MEDIA_URL
    })


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

def create_listing(request):
    if request.method == "POST":
        listing_form = AddListingForm(request.POST, request.FILES)
        if listing_form.is_valid():
            listing_form.save()
            return redirect('success')
        #return HttpResponseRedirect(reverse("index"))
    else:
        add_listing_form = AddListingForm()
        return render(request, 'auctions/create_listing.html', {
            'add_listing_form': add_listing_form
        })  
  
def success(request):
    return HttpResponse('successfully uploaded')       

def listing(request, title):
    model = Listing.listings.get(listing_name=title)
    # if Bid.bids.get(listing_id=model.listing_id):
    #     bid_model = Bid.bids.get(listing_id=model.listing_id)
    # else:
    #     bid_model  
    bid = BidsForm(initial={'placed_bid': model.starting_bid})
    #bid.initial(amount_bid=model.starting_bid)
    if request.method=='POST':
        placed_bid = float(request.POST.get("placed_bid"))
        user_name = None
        
        if request.user.is_authenticated:
            user_name = request.user.username
            name = User.objects.get(username=user_name)
            # listing_id = model.listing_id
            if model.starting_bid < placed_bid:
                model.starting_bid = placed_bid
                model.save()
                bid_accepted = Bid(listing_id=model, username=name,amount_bid=placed_bid)
                bid_accepted.save()
            
            return HttpResponseRedirect(reverse("index"))
    else:
        past_bids = Bid.bids.filter(listing_id=model)
        return render(request, "auctions/listing.html", {
        "listing": model,
        'media_url': settings.MEDIA_URL,
        'bid_form': bid,
        'previous_bids': past_bids
        })

def category(request, cat):
    category_list = Listing.listings.filter(listing_cat=cat)
    return render(request, "auctions/index.html", {
        'listings': category_list,
        'media_url': settings.MEDIA_URL
    })

def categories(request):
    categories = Listing.listings.all()
    dist_cats = []
    for listing in categories:
        if listing.listing_cat not in dist_cats:
            dist_cats.append(listing.listing_cat)
    return render(request, "auctions/categories.html", {
        'categories': dist_cats
    })