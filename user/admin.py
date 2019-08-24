from django.contrib import admin
from .form import MyUserChangeForm, MyUserCreationForm
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

class MyAdminClass(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser
    list_display = [ 'username', 'job']

admin.site.register(MyUser, MyAdminClass)

