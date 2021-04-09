from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils.timezone
from django.utils.translation import ugettext as _

from .utils import now_plus_7
from django.db.models.signals import post_delete
import os
from django.dispatch import receiver

# ... models code goes here ...

# Using ManyToManyField relations and properties:

# class MyDjangoClass(models.Model):
#     name = models.CharField(...)
#     friends = models.ManyToManyField("self")

#     @property
#     def friendlist(self):
#         # Watch for large querysets: it loads everything in memory
#         return list(self.friends.all())
# You can access a user's friend list this way:

# joseph = MyDjangoClass.objects.get(name="Joseph")
# friends_of_joseph = joseph.friendlist

#if class added must run python manage.py makemigrations
# then run python manage.py migrate
# python createsuperuser
#username: kaw
#password: Arthur

# auction listings, bids, comments, and auction

# Your application should have at least three models in addition to the User model: 
# one for auction listings, 
# one for bids, 
# one for comments made on auction listings. 

class User(AbstractUser):
    pass



class Listing(models.Model):
    # underscore is a function that allows for translating to native language.
    # Textchoice is an enumeration type for text based options
    class Categories(models.TextChoices):
        FASHION = 'FSH', _('Fashion')
        TOYS = 'TOY', _('Toys')
        ELECTRONICS = 'ELC', _('Electronics')
        HOME = 'HOM', _('Home')
        ART = 'ART', _('Art')
        LITERATURE = 'LIT', _('Literature')
        # FASHION = _('Fashion')
        # TOYS =  _('Toys')
        # ELECTRONICS = _('Electronics')
        # HOME = _('Home')
        # ART = _('Art')
        # LITERATURE = 'LIT', _('Literature')
    listing_id   = models.AutoField(primary_key=True)
    listing_cat  = models.CharField(max_length=20, choices=Categories.choices, default=Categories.HOME)
    #listing_id  = models.IntegerField(primary_key=True, auto_created=True)
    listing_name = models.CharField(max_length=100)
    description  = models.CharField(max_length=200, default="please provide a description")
    close_date   = models.DateTimeField(default=now_plus_7())
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    listing_img  = models.ImageField(upload_to='images/', null=True, blank=True)
    #used instead of objects to access data in db of this model
    listings = models.Manager()
    users_watching = models.ManyToManyField(User)

    def __str__(self): 
       return self.listing_name

class Bid(models.Model): 
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_bid = models.DecimalField(max_digits=8, decimal_places=2)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bids = models.Manager()
    def __str__(self): 
        return f"User:{self.username} bids {self.amount_bid} on item no: {self.listing_id}."

class Listing_Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)

    def __str__(self): 
        return f"User:{self.username} commented on item no: {self.listing_id}."

#deletes associated photos when model listing is deleted.

def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

@receiver(models.signals.post_delete, sender=Listing)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.listing_img:
        _delete_file(instance.listing_img.path)