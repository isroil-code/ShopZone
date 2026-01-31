from django.db import transaction

@transaction.atomic
def get_or_create_product(seller):
    from .models import Product
    product, _ = Product.objects.get_or_create(seller=seller)
    return product