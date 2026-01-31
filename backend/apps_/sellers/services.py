from django.db import transaction

@transaction.atomic
def create_shartnoma(seller):
    from .models import Shartnoma
    shartnoma = Shartnoma.objects.create(seller=seller)
    return shartnoma    

@transaction.atomic
def create_seller_balnce(seller):
    from .models import SellerBalance
    balance = SellerBalance.objects.create(seller=seller)
    return balance


