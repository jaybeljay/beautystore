from django.urls import path

from .views import cart_adding, FavoriteView, delete_item, favorites, checkout
from .models import FavoriteProduct

urlpatterns = [
    path('cart_adding/', cart_adding, name='cart_adding'),
    path('checkout/', checkout, name='checkout'),
    path('favorites', favorites, name='favorites'),
    path('favorite/', FavoriteView.as_view(model=FavoriteProduct), name='favorite'),
    path('delete_item/', delete_item, name='delete_item'),
]
