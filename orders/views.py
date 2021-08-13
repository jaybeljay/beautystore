import json
import decimal

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views import View

from main.models import Profile
from products.models import Product
from .models import Status, Order, ProductInOrder, ProductInCart, FavoriteProduct
from .forms import CheckoutForm


def cart_adding(request):
    return_dic = dict()
    data = request.POST
    product_id = data.get('product_id')
    nmb = data.get('nmb')
    
    new_product, created = ProductInCart.objects.get_or_create(user=request.user, product_id=product_id, defaults={"nmb": nmb})
    if not created:
        new_product.nmb += int(nmb)
        new_product.save(force_update=True)
    
    products_in_cart = ProductInCart.objects.filter(user=request.user, is_active=True)
    products_total_nmb = products_in_cart.count()
    return_dic['products_total_nmb'] = products_total_nmb
    return_dic['products'] = list()
    
    for item in products_in_cart:
        product_dict = dict()
        product_dict["name"] = item.product.name
        product_dict["price"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dic["products"].append(product_dict)
    
    return JsonResponse(return_dic)  


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class FavoriteView(View):
    model = None
    
    def post(self, request):
        user = request.user
        product_id = request.POST.get('obj')
        favorite, created = self.model.objects.get_or_create(user=user, obj_id=product_id)
        if not created:
            favorite.delete()
            
        favorites_in_cart = self.model.objects.filter(user=user)
        favorites_nmb = favorites_in_cart.count()
        favorites = list()
    
        for item in favorites_in_cart:
            favorite_dict = dict()
            favorite_dict["name"] = item.obj.name
            favorite_dict["price"] = item.obj.price
            favorites.append(favorite_dict)
        
        return HttpResponse(
            json.dumps({
                'result': created,
                'count': favorites_nmb,
                'favorites': favorites
            }, cls = DecimalEncoder),
            content_type = 'application/json',
        )


def delete_item(request):
    user = request.user
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
    products_in_cart = ProductInCart.objects.filter(user=request.user, is_active=True)
    form = CheckoutForm(request.POST or None)
    profile = Profile.objects.get(user=request.user)
    
    if request.POST:
        if form.is_valid():
            first_name = form.cleaned_data['user_first_name']
            last_name = form.cleaned_data['user_last_name']
            phone = form.cleaned_data['user_phone']
            address = form.cleaned_data['user_address']
            comments = form.cleaned_data['comments']
            
            order = Order.objects.create(user=request.user, user_first_name=first_name, user_last_name=last_name, 
            user_phone=phone, user_address=address, comments=comments, status_id=1)
            
            for name, value in request.POST.items():
                if name.startswith('product_'):
                    product_in_cart_id = name.split('product_')[1]
                    product_in_cart = ProductInCart.objects.get(id=product_in_cart_id)
                    product_in_cart.nmb = value
                    product_in_cart.save(force_update=True)
                    
                    ProductInOrder.objects.create(order=order, product=product_in_cart.product, nmb=product_in_cart.nmb, 
                    price_per_item=product_in_cart.price_per_item, total_price = product_in_cart.total_price)

    return render(request, 'orders/checkout.html', {'products_in_cart': products_in_cart, 'form': form, 'profile': profile})
