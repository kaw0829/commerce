from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
#make sure pattern doesnt trigger any previous patterns when adding  'watchlist' was triggering <cat> without /
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="add_listing"),
    path('success', views.success, name = 'success'),
    path('listing/<title>', views.listing, name='listing'),
    path("categories", views.categories, name='categories'),
    path("<cat>", views.category, name='category'),
    path("watchlist/<listing>", views.watchlist, name='watchlist'),
    path("watchlist/", views.watchlist, name='watchlist')
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)