from django.db import models
from django.utils.text import slugify

from user_module.models import User


# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام دسته بندی')
    slug = models.SlugField(max_length=100, verbose_name='عنوان در url', unique=True)
    parent = models.ForeignKey('ProductCategory', verbose_name='والد', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال', default=True)

    class Meta:
        verbose_name = 'دسته بندی محصولات'
        verbose_name_plural = 'دسته بندی های محصولات'

    def __str__(self):
        return self.name

class ProductBrand(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام برند')
    slug = models.SlugField(max_length=100, verbose_name='عنوان در url', unique=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام محصول')
    price = models.IntegerField(verbose_name='قیمت محصول')
    category = models.ForeignKey(ProductCategory, verbose_name='دسته بندی', on_delete=models.CASCADE)
    brand = models.ForeignKey(ProductBrand, verbose_name='برند', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/products', verbose_name='تصویر', null=True, blank=True)
    short_description = models.CharField(max_length=400, verbose_name='توضیحات کوتاه')
    descriptions = models.TextField(verbose_name='توضیحات')
    slug = models.SlugField(verbose_name='عنوان در url', unique=True, max_length=100, db_index=True, allow_unicode=True)
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال', default=True)
    is_available = models.BooleanField(verbose_name='موجود / غیر موجود', default=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return f'({self.name} : {self.price})'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class ProductComment(models.Model):
    comment = models.TextField(verbose_name='کامنت')
    user = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE)
    parent = models.ForeignKey('ProductComment', null=True, blank=True, verbose_name='والد', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ثبت')

    def __str__(self):
        return f'{self.product}: {self.comment}'

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'


class LikeComment(models.Model):
    user = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.CASCADE)
    comment = models.ForeignKey(ProductComment, verbose_name='کامنت', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'comment')
        verbose_name = 'لایک نظر'
        verbose_name_plural = 'لایک های نظر'

    def __str__(self):
        return f'{self.comment}'


class ProductSpecifications(models.Model):
    title = models.CharField(verbose_name='عنوان ویژگی', max_length=100)
    value = models.CharField(verbose_name='ویژگی', max_length=200)
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'شاخصه'
        verbose_name_plural = 'مشخصات'

    def __str__(self):
        return f'({self.title}: {self.value})'
