from django.contrib import admin
from .models import Item


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description', 'price']
    list_display = ['name', 'price']
    list_filter = ['price']


admin.site.register(Item, ItemAdmin)
