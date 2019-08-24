from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Items, Order, OrderItem, Address
from .serializer import ListItemsSerializer, OrderSerializer, OrderItemSerializer
from .paginator import ShopPaginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers.userSeriliazer import MyUserSeriliazer



class ListItems(generics.ListAPIView):
    queryset = Items.objects.all()
    serializer_class = ListItemsSerializer
    pagination_class = ShopPaginator

class SingleItem(generics.RetrieveAPIView):
    lookup_field = 'pk'
    queryset = Items.objects.all()
    serializer_class = ListItemsSerializer

class AddToCart(APIView):
    def post(self, request, pk):
        item = get_object_or_404(Items, pk = pk)
        order_item, created = OrderItem.objects.get_or_create(
            user =request.user,
            item = item,
            ordered = False
        )
        order_qs = Order.objects.filter(user = request.user, ordered = False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderItem.filter(item__id = item.id).exists():
                order_item.quantity += 1
                order_item.save()
                order_ser = OrderSerializer(order)
                return  Response(order_ser.data, status=status.HTTP_200_OK)
            else:
                order.orderItem.add(order_item)
                order_ser = OrderSerializer(order)
                return  Response(order_ser.data, status=status.HTTP_200_OK)
        else:
            order_date = timezone.now()
            order = Order.objects.create(
                ordered_date = order_date,
                user = request.user,
                ordered = False
            )
            order.orderItem.add(order_item)
            order_ser = OrderSerializer(order)
            return  Response(order_ser.data, status=status.HTTP_200_OK)


class GetOrder(APIView):
    def get(self, request):
        order_qs = Order.objects.filter(user = request.user, ordered = False)
        if order_qs.exists():
            order = order_qs[0]
            order_ser = OrderSerializer(order)
            return  Response(order_ser.data, status=status.HTTP_200_OK)
        else:
            return  Response({'orderItem':0}, status=status.HTTP_200_OK)

class RemoveFromCart(APIView):
    def post(self, request, pk):
        item = get_object_or_404(Items, pk = pk)
        order_qs =Order.objects.filter(
        user = request.user,
        ordered = False
        )
        if order_qs.exists():
            order = order_qs[0]
            if order.orderItem.filter(item__id = item.id).exists():
                order_item = OrderItem.objects.filter(
                    user = request.user,
                    item = item,
                    ordered = False
                )[0]
                print(order)
                order.orderItem.remove(order_item)
                order_item.delete()
                if not order.orderItem.count():
                    order_qs.delete()
                order_ser = OrderSerializer(order)
                return  Response(order_ser.data, status=status.HTTP_200_OK)
            else:
                order_ser = OrderSerializer(order)
                return  Response(order_ser.data, status=status.HTTP_200_OK)
        else:
            order_ser = OrderSerializer(order)
            return  Response(order_ser.data, status=status.HTTP_200_OK)

class Remove_single_item(APIView):
    def post(self, request, pk):
        item = get_object_or_404(Items, pk = pk)
        order_item = OrderItem.objects.get(
            user = request.user,
            item = item,
            ordered = False
        )
        order_qs =Order.objects.filter(
                user = request.user,
                ordered = False
            )[0]
        order_item.quantity -= 1
        if not order_item.quantity:
            order_qs.orderItem.remove(order_item)
            order_item.delete()
        else:
            order_item.save()
        order_ser = OrderSerializer(order_qs)
        return  Response(order_ser.data, status=status.HTTP_200_OK)

class Checkout(APIView):
    def post(self, request):
        data = request.data["formData"]
        if data["default_address"]:
            address, created = Address.objects.update_or_create(
                user =request.user,
                default_address = True,
                defaults = {
                'email' : data["email"],
                'country' : data["country"],
                'address' : data["address"],
                'zip' : data["zip"],
                'payment_method' : data["payment_method"]
                }
            )
            order = Order.objects.filter(
                    user = request.user,
                    ordered = False
                ).first()
            order.address = address
            order.save()
            order_ser = OrderSerializer(order)
            return  Response(order_ser.data, status=status.HTTP_200_OK)
        else:
            default = False
            address =  Address(
                user = request.user,
                email = data["email"],
                country = data["country"],
                address = data["address"],
                zip = data["zip"],
                default_address = default,
                payment_method = data["payment_method"]
            )
            address.save()
            order = Order.objects.filter(
                user = request.user,
                ordered = False
            ).first()
            order.address = address
            order.save()
            order_ser = OrderSerializer(order)
            return  Response(order_ser.data, status=status.HTTP_200_OK)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        us = MyUserSeriliazer(self.user)
        # Add extra responses here
        data['user'] = us.data
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




