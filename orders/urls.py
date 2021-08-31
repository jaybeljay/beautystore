from django.urls import path

from .views import cart_adding, favorite_adding, delete_item, favorites, checkout

urlpatterns = [
    path('cart_adding/', cart_adding, name='cart_adding'),
    path('checkout/', checkout, name='checkout'),
    path('favorites', favorites, name='favorites'),
    path('favorite/', favorite_adding, name='favorite'),
    path('delete_item/', delete_item, name='delete_item'),
]
