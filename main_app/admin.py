from django.contrib import admin
from .models import Photo, Recipe, Review, Item, ShoppingList

# Register your models here.
admin.site.register(Review)
admin.site.register(Item)
admin.site.register(ShoppingList)
admin.site.register(Recipe)
admin.site.register(Photo)
