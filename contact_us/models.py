from django.db import models
from user_module.models import User


# Create your models here.


class ContactUsModel(models.Model):
    STATUS_CHOICES = [
        ('new', 'جدید'),
        ('read', 'خوانده شده'),
        ('answer', 'پاسخ داده شده'),
        ('closed', 'بسته شده'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='message_user')
    full_name = models.CharField(max_length=200, verbose_name='نام و نام خانوادگی')
    email = models.EmailField(max_length=200, verbose_name='ایمیل')
    subject = models.CharField(max_length=100, verbose_name='موضوع')
    message = models.TextField(verbose_name='پیام')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال پیام', editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='وضعیت')

    admin_reply = models.TextField(verbose_name='پاسخ ادمین', null=True, blank=True)
    replied_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cmessage_replied_by_admin')
    replied_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'پیام ارتباط با ما'
        verbose_name_plural = 'پیام های ارتباط با ما'

    def __str__(self):
        return f'{self.full_name} - {self.message}'