from .models import ProductInCart, FavoriteProduct, Order, ProductInOrder


def add_product_to_cart(user, product_id, nmb):
    new_product, created = ProductInCart.objects.get_or_create(user=user, product_id=product_id, defaults={"nmb": nmb})
    if not created:
        new_product.nmb += int(nmb)
        new_product.save(force_update=True)


def show_cart(user):
    return_dic = dict()
    products_in_cart = ProductInCart.objects.filter(user=user, is_active=True)
    products_total_nmb = products_in_cart.count()
    return_dic['products_total_nmb'] = products_total_nmb
    return_dic['products'] = list()
    
    for item in products_in_cart:
        product_dict = dict()
        product_dict["name"] = item.product.name
        product_dict["price"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dic["products"].append(product_dict)
        
    return return_dic
    
    
def add_product_to_favorite(user, product_id):
    favorite, created = FavoriteProduct.objects.get_or_create(user=user, obj_id=product_id)
    if not created:
        favorite.delete()
    

def show_favorite(user):
    return_dic = dict()
    favorites_in_cart = FavoriteProduct.objects.filter(user=user)
    favorites_nmb = favorites_in_cart.count()
    return_dic['favorites_nmb'] = favorites_nmb
    return_dic['favorites'] = list()

    for item in favorites_in_cart:
        favorite_dict = dict()
        favorite_dict["name"] = item.obj.name
        favorite_dict["price"] = item.obj.price
        return_dic['favorites'].append(favorite_dict)
    
    return return_dic
    
    
def create_order(user, form):
    first_name = form.cleaned_data['user_first_name']
    last_name = form.cleaned_data['user_last_name']
    phone = form.cleaned_data['user_phone']
    address = form.cleaned_data['user_address']
    comments = form.cleaned_data['comments']
    
    order = Order.objects.create(user=user, user_first_name=first_name, user_last_name=last_name,
            user_phone=phone, user_address=address, comments=comments, status_id=1)
            
    return order


def add_product_to_order(request, order_pk):
    
    order = Order.objects.get(pk=order_pk)
    
    for name, value in request.POST.items():
        if name.startswith('product_'):
            product_in_cart_id = name.split('product_')[1]
            product_in_cart = ProductInCart.objects.get(id=product_in_cart_id)
            product_in_cart.nmb = value
            product_in_cart.save(force_update=True)
            
            ProductInOrder.objects.create(order=order, product=product_in_cart.product, nmb=product_in_cart.nmb,
            price_per_item=product_in_cart.price_per_item, total_price=product_in_cart.total_price)
