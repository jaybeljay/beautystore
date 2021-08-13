from django.urls import path

from .views import home, product_category, product, SearchView, reset_btn

urlpatterns = [
    path('', home, name = 'home'),
    path('product/category/<slug:slug>', product_category, name='category'),
    path('product/<product_id>', product, name='product'),
    path('search/', SearchView.as_view(), name='search'),
    path('reset/', reset_btn, name='reset'),
]
