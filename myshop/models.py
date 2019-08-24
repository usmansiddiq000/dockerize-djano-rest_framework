from django.db import models
from django.conf import settings

class Items(models.Model):
    name = models.CharField(max_length = 50)
    tag = models.CharField(max_length = 50)
    title = models.CharField(max_length = 50)
    price = models.FloatField()
    image = models.FileField(upload_to= 'images/')

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    item = models.ForeignKey(Items, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default= False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank = True, null=True) 
    address =models.CharField(max_length = 255)
    zip = models.CharField(max_length = 30)
    country =models.CharField(max_length = 30)
    email = models.CharField(max_length = 50)
    payment_method = models.CharField(max_length = 10)
    default_address = models.BooleanField(default= False)


    def __str__(self):
        return self.address


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    orderItem = models.ManyToManyField(OrderItem)
    address = models.ForeignKey(Address, on_delete = models.CASCADE, null = True)
    ordered = models.BooleanField(default= False)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return self.user.username



