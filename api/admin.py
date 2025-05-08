from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, OrderItem, Order


# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)