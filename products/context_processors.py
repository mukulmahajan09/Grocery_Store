from products.models import ProductCategory

def menu_links(request):
    links = ProductCategory.objects.all()
    return dict(links=links)