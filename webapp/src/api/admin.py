from django.contrib import admin
from .models import Item, Order, Tax, Discount


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description', 'price']
    list_display = ['name', 'price']
    list_filter = ['price']


admin.site.register(Item, ItemAdmin)
admin.site.register(Order)
admin.site.register(Tax)
admin.site.register(Discount)
