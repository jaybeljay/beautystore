import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from main.models import Profile
from .models import ProductInCart, FavoriteProduct
from .forms import CheckoutForm
from .services import add_product_to_cart, show_cart, add_product_to_favorite, show_favorite, create_order, add_product_to_order
from .utils import DecimalEncoder


def cart_adding(request):
    add_product_to_cart(request.user, request.POST['product_id'], request.POST['nmb'])
    cart = show_cart(request.user)
    return JsonResponse(cart)


def favorite_adding(request):
    add_product_to_favorite(request.user, request.POST['obj'])
    favorite = show_favorite(request.user)
    
    return HttpResponse(
        json.dumps(favorite, cls=DecimalEncoder),
        content_type='application/json',
    )


def delete_item(request):
    data = json.loads(request.body.decode("utf-8"))
    item_id = data.get('item_id')
    item_type = data.get('item_type')
    
    if item_type == 'favoriteproduct':
        favorite = FavoriteProduct.objects.get(id=item_id)
        favorite.delete()
        return HttpResponse(json.dumps({'result': 'Deleted'}), content_type='application/json')
    elif item_type == 'cartproduct':
        product = ProductInCart.objects.get(id=item_id)
        product.delete()
        return HttpResponse(json.dumps({'result': 'Deleted'}), content_type='application/json')


def favorites(request):
    favorites_in_cart = FavoriteProduct.objects.filter(user=request.user)
    return render(request, 'orders/favorites.html', {'favorites_in_cart': favorites_in_cart})


def checkout(request):
    form = CheckoutForm(request.POST or None)
    profile = Profile.objects.get(user=request.user)
    products_in_cart = ProductInCart.objects.filter(user=request.user, is_active=True)
    
    if request.POST:
        if form.is_valid():
            order = create_order(request.user, form)
            add_product_to_order(request, order.pk)

    return render(request, 'orders/checkout.html', {'products_in_cart': products_in_cart, 'form': form, 'profile': profile})
