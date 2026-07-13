from django.db import models

# Create your models here.


class SiteSettings(models.Model):
    site_name = models.CharField(verbose_name='نام سایت', max_length=100)
    site_url = models.URLField(verbose_name='دامنه سایت', max_length=200, unique=True)
    phone = models.CharField(verbose_name='تلفن', max_length=20)
    address = models.TextField(verbose_name='آدرس')
    email = models.EmailField(verbose_name='ایمیل', max_length=20, unique=True)
    copyright = models.TextField(verbose_name='متن کپی رایت سایت')
    about_us_text = models.TextField(verbose_name='متن درباره ما سایت')
    site_logo = models.ImageField(upload_to='images/site-setting/', verbose_name='لوگو سایت')
    is_main_setting = models.BooleanField(verbose_name='تنظیمات اصلی')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.site_name