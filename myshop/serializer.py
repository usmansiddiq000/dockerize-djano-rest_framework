from rest_framework import serializers
from .models import Items, Order, OrderItem, Address
from django.conf import settings

class ListItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Items
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
     item = serializers.PrimaryKeyRelatedField(queryset=Items.objects.all())
     def to_representation(self, value):
        data = super().to_representation(value)
        d = ListItemsSerializer(value.item)
        data['item'] = d.data
        return data
     class Meta:
         model = OrderItem
         fields = ( 'item','quantity', 'ordered')


class OrderSerializer(serializers.ModelSerializer):
    orderItem = serializers.PrimaryKeyRelatedField(queryset=OrderItem.objects.all(), many=True)
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
    def to_representation(self, value):
        data = super().to_representation(value)
        data['orderItem'] = []
        for item in value.orderItem.all():
            d = OrderItemSerializer(item)
            data['orderItem'].append(d.data)
        return data
    class Meta:
        model = Order
        fields = ( 'address', 'orderItem', 'start_date', 'ordered_date', 'ordered')


