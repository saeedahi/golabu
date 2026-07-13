from django.contrib import admin
from . import models

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'slug']
    list_editable = ['price', 'slug']

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductBrand)
admin.site.register(models.ProductComment)
admin.site.register(models.LikeComment)
admin.site.register(models.ProductSpecifications)