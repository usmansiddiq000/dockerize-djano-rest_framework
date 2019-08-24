
from django.urls import path, include
from rest_framework import routers
from .views import ListItems,SingleItem,AddToCart, GetOrder, RemoveFromCart, Remove_single_item, Checkout

urlpatterns = [
    path('list/', ListItems.as_view()),
    path('<int:pk>', SingleItem.as_view()),
    path('add-to-cart/<int:pk>', AddToCart.as_view()),
    path('get-order/', GetOrder.as_view()),
    path('remove-from-cart/<int:pk>', RemoveFromCart.as_view()),
    path('remove-single-item/<int:pk>', Remove_single_item.as_view()),
    path('checkout', Checkout.as_view())
]
