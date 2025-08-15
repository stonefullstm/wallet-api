from django.contrib import admin
from .models import Stock
from user.models import User


# Register your models here.
admin.site.register(Stock)
admin.site.register(User)
