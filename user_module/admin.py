from django.contrib import admin
from user_module import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.UserAddress)