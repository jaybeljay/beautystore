from .models import ProductCategory


def display_categories(request):
    categorlist = ProductCategory.objects.values_list('name', 'slug', named=True)
    return {
        'categorlist': categorlist
    }
