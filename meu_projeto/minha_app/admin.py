from django.contrib import admin
from .models import User, Profile, Product, Order

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Order)
