from django.contrib import admin
from .models import Item, Order, Tax, Discount


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description', 'price', 'currency']
    list_display = ['name', 'price', 'currency']
    list_filter = ['price', 'currency']


admin.site.register(Item, ItemAdmin)
admin.site.register(Order)
admin.site.register(Tax)
admin.site.register(Discount)
