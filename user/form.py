from django.forms import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import MyUser

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = MyUser
        fields = ('username', 'email', 'job')

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = MyUser
        fields = UserChangeForm.Meta.fields