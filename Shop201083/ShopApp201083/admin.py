from django.contrib import admin
from .models import Product, ShopUser, Order, OrderItem, Delivery

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True


admin.site.register(Product, ProductAdmin)

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Delivery)
admin.site.register(ShopUser)

