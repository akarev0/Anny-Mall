from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from .models import Category, Customer, Basket


class CategoryDetailMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class BasketMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            basket = Basket.objects.filter(owner=customer, in_order=False).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )

            if not basket:
                basket = Basket.objects.create(owner=customer)
        else:
            basket = Basket.objects.filter(for_anonymous_user=True).first()
            if not basket:
                basket = Basket.objects.create(for_anonymous_user=True)

        self.basket = basket
        return super(BasketMixin, self).dispatch(request, *args, **kwargs)
