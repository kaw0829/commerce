from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext as _

from .models import User, Listing, Listing_Comment, Bid

# ModelForm takes a model and creates a form,  has a .save method to save to post data to db.

class AddListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["listing_cat", "listing_name","description", "close_date", "listing_img"]
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

def index(request):
    return render(request, "auctions/index.html")


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