from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.contrib.sessions.backends.db import SessionStore
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

            if not customer:
                customer = Customer.objects.create(user=request.user)
            basket = Basket.objects.filter(owner=customer, in_order=False).first()

            if not basket:
                basket = Basket.objects.create(owner=customer)
        else:
            session = SessionStore(session_key=request.COOKIES.get('session_key'))
            if session.session_key is None:
                session.create()
                self.session = session

            self.session = session

            basket = Basket.objects.filter(session_id=session.session_key).first()

            if not basket:
                basket = Basket.objects.create(session_id=session.session_key, for_anonymous_user=True)
        self.basket = basket

        return super().dispatch(request, *args, **kwargs)
