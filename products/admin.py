from django.contrib import admin

from .models import ProductCategory, Product

    
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductCategory._meta.fields]
    
    class Meta:
        model = ProductCategory
    
admin.site.register(ProductCategory, ProductCategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    
    class Meta:
        model = Product
    
admin.site.register(Product, ProductAdmin)
