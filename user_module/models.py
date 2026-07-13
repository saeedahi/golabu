from django.db import models
from django.contrib.auth.models import AbstractUser
from iranian_cities.models import Province, County

# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(unique=True, verbose_name='شماره همراه', null=True, blank=True)
    active_phone_number = models.CharField(null=True, blank=True, verbose_name='کد فعالسازی شماره')
    email_active_code = models.CharField(null=True, blank=True, max_length=100, verbose_name='کد فعالسازی ایمیل')
    about_user = models.TextField(null=True, blank=True, verbose_name='درباره کاربر')

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


class UserAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    province = models.ForeignKey(Province, on_delete=models.PROTECT, verbose_name='استان')
    county = models.ForeignKey(County, on_delete=models.PROTECT, verbose_name='شهرستان')
    district = models.CharField(max_length=200, verbose_name='محله / شهرک')
    street = models.CharField(max_length=200, verbose_name='خیابان / کوچه')
    building = models.CharField(max_length=200, verbose_name='ساختمان', null=True, blank=True)
    number_plate = models.IntegerField(verbose_name='شماره پلاک')
    postal_code = models.CharField(max_length=10, verbose_name='کد پستی')
    full_address = models.TextField(verbose_name='آدرس کامل', null=True, blank=True)

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'

    def __str__(self):
        return f'{self.user}: {self.province}'
