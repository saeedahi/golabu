from django.contrib import admin
from django.utils import timezone

from contact_us import models

# Register your models here.

@admin.register(models.ContactUsModel)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'subject', 'created_at', 'status']

    readonly_fields = ['created_at']

    def save_model(self, request, obj: models.ContactUsModel, form, change):
        if obj.admin_reply and obj.status != 'answer':
            obj.status = 'answer'
            obj.replied_by = request.user
            obj.replied_at = timezone.now()

        super().save_model(request, obj, form, change)


# admin.site.register(models.ContactUsModel, ContactUsAdmin)