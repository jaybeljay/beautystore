from django.db.models import Sum

from .models import ProductInCart, FavoriteProduct


def get_cart_info(request):
    if request.user.is_authenticated:
        products_in_cart = ProductInCart.objects.filter(user=request.user, is_active=True)
        if products_in_cart:
            return {'products_in_cart': products_in_cart, 'products_total_nmb': products_in_cart.aggregate(Sum('nmb'))['nmb__sum']}
        return {'products_in_cart': None, 'products_total_nmb': None}
    else:
        return {'products_in_cart': None, 'products_total_nmb': None}
    

def get_favorite_count(request):
    if request.user.is_authenticated:
        user_favorites = FavoriteProduct.objects.filter(user=request.user)
        if user_favorites:
            return {'favorites_nmb': user_favorites.count(), 'user_favorites': user_favorites}
        return {'favorites_nmb': None, 'user_favorites': None}
    else:
        return {'favorites_nmb': None, 'user_favorites': None}
