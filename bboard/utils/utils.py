from django.db import models


def refresh_basket(basket):
    basket_data = basket.products.aggregate(models.Sum('total_cost'), models.Count('id'))
    if basket_data.get('total_cost__sum'):
        basket.total_cost = basket_data.get('total_cost__sum')
    else:
        basket.total_cost = 0

    basket.total_products_in_basket = basket_data.get('id__count')
    basket.save()
