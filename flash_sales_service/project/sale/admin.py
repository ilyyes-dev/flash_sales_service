from django.contrib import admin

from .models import IdempotencyKey, Order, Product


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(IdempotencyKey)