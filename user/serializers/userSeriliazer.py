from rest_framework import serializers
from user.models import MyUser

class MyUserSeriliazer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("id","last_login",
        "is_superuser",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
        "job",
        "groups",
        "user_permissions") 