from .models import ECommerceBalance


def add_to_balance(amount):
    balance_obj = ECommerceBalance.objects.get(id=1)
    balance_obj.balance += amount
    balance_obj.save(update_fields=['balance'])
    return balance_obj.balance

