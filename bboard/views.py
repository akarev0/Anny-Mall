from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    DetailView,
    View, TemplateView
)

from anny_mall import settings
from anny_mall.liqpay import LiqPay
from .mixins import CategoryDetailMixin, BasketMixin
from .models import (
    Product,
    Category,
    BasketProduct,
    Customer,
    Order
)

from .forms import OrderForm
from .utils.utils import refresh_basket


class BaseView(BasketMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {
            'categories': categories,
            'products': products,
            'basket': self.basket
        }
        return render(request, "bboard/base.html", context=context)


class ProductDetailView(CategoryDetailMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'bboard/item_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context


class CategoryDetailView(CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'bboard/category_detail.html'
    slug_url_kwarg = 'slug'


class BasketView(BasketMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'basket': self.basket,
            'categories': categories
        }

        return render(request, 'bboard/basket.html', context=context)


class AddToBasketView(BasketMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        basket_product, created = BasketProduct.objects.get_or_create(
            user=self.basket.owner,
            basket=self.basket,
            product=product
        )

        self.basket.products.add(basket_product)
        refresh_basket(self.basket)
        return HttpResponseRedirect('/basket/')


class DeleteFromBasketView(BasketMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        basket_product = BasketProduct.objects.get(
            user=self.basket.owner,
            basket=self.basket,
            product=product
        )

        self.basket.products.remove(basket_product)

        refresh_basket(self.basket)
        return HttpResponseRedirect('/basket/')


class CheckOutView(BasketMixin, View):

    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        categories = Category.objects.all()
        context = {
            'basket': self.basket,
            'categories': categories,
            'form': form
        }

        return render(request, 'bboard/checkout.html', context=context)


class MakeOrderView(BasketView, View):
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.basket.in_order = True
            refresh_basket(self.basket)
            new_order.basket = self.basket
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/pay/')
        return HttpResponseRedirect('/checkout/')


class PayView(TemplateView):

    def get(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.filter(customer=customer.id).first()
        params = {
            'action': 'pay',
            'amount': int(order.basket.total_cost),
            'currency': 'UAH',
            'description': order.comment,
            'order_id': order.id,
            'version': '3',
            'sandbox': 0,
            'server_url': 'http://localhost:8000/pay-callback/',
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        return render(request, 'bboard/payment.html', {'signature': signature, 'data': data})


@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
        if sign == signature:
            print('callback is valid')
        response = liqpay.decode_data_from_str(data)
        print('callback data', response)
        return HttpResponse()


class AboutPage(View):

    def get(self, request):
        return render(request, "bboard/about_us.html")
