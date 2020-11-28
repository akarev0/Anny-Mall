from django.urls import path

from .views import (
    ProductDetailView,
    CategoryDetailView,
    BaseView,
    BasketView,
    AddToBasketView,
    DeleteFromBasketView,
    CheckOutView,
    AboutPage, MakeOrderView
)

urlpatterns = [
    path("", BaseView.as_view(), name="home_page"),
    path("about/", AboutPage.as_view(), name="about-page"),
    path('products/<str:slug>/', ProductDetailView.as_view(), name='item_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('add-to-basket/<str:slug>/', AddToBasketView.as_view(), name='add_to_basket'),
    path('delete-from-basket/<str:slug>/', DeleteFromBasketView.as_view(), name='delete_from_basket'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='order')

]
