from django.shortcuts import render, redirect
from django.db.models import Q, Min, Max
from django.views.generic import ListView
from django.urls import reverse

from .models import Product, ProductCategory


def home(request):
    products = Product.objects.filter(is_active=True).reverse()[:4]
    return render(request, 'products/home.html', {'products': products})


def product_category(request, slug):
    category = ProductCategory.objects.get(slug=slug)
    products_active = Product.objects.filter(is_active=True)
    products = products_active.filter(category__slug=slug)
    return render(request, 'products/category.html', {'products': products, 'category': category})


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'products/product.html', {'product': product})
    

class SearchView(ListView):
    model = Product
    template_name = 'products/search.html'
    context_object_name = 'products'
    paginate_by = 20
    count = 0
    
    def get_queryset(self):
        products = Product.objects.all()
        categories = ProductCategory.objects.all()
        min_price = products.aggregate(minprice=Min('price'))
        max_price = products.aggregate(maxprice=Max('price'))
        query_text = self.request.GET.get('q-text')
        query_price_min = self.request.GET.get('q-price-min')
        query_price_max = self.request.GET.get('q-price-max')
        query_cat = self.request.GET.get('q-cat')
        
        def is_valid_param(param):
            return param != '' and param is not None
        
        if is_valid_param(query_text):
            products = products.filter(Q(name__icontains=query_text) | Q(description__icontains=query_text)).distinct()
            
        if is_valid_param(query_price_min):
            products = products.filter(Q(price__gte=query_price_min))
            
        if is_valid_param(query_price_max):
            products = products.filter(Q(price__lte=query_price_max))
            
        if is_valid_param(query_cat) and query_cat != 'Choose...':
            products = products.filter(Q(category__name=query_cat))
        
        return products
    
    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        context['categories'] = ProductCategory.objects.all()
        context['minprice'] = Product.objects.all().aggregate(minprice=Min('price'))
        context['maxprice'] = Product.objects.all().aggregate(maxprice=Max('price'))
        return context
        

def reset_btn(request):
    return redirect(reverse('search'))
