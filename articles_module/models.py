from ckeditor.fields import RichTextField
from django.db import models
from user_module.models import User
from utils.for_blogs import add_heading_ids, calculate_reading_time
from django.utils.text import slugify


# Create your models here.

class ArticleCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='نام دسته بندی')
    url_title = models.SlugField(max_length=100, verbose_name='عنوان در url', db_index=True, allow_unicode=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def save(self, *args, **kwargs):
        self.url_title = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class ArticleTags(models.Model):
    tag = models.CharField(max_length=200, verbose_name='تگ')
    in_url = models.SlugField(db_index=True, max_length=200, verbose_name='عنوان در url', allow_unicode=True, editable=False)

    def __str__(self):
        return self.in_url

    class Meta:
        verbose_name = 'تگ مقاله'
        verbose_name_plural = 'تگ های مقاله'

    def save(self, *args, **kwargs):
        self.in_url = slugify(self.tag, allow_unicode=True)
        super().save(*args, **kwargs)


class ArticleModel(models.Model):
    title = models.CharField(max_length=300, verbose_name="عنوان مقاله")
    category = models.ForeignKey(ArticleCategory, verbose_name='دسته بندی', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(db_index=True, max_length=300, verbose_name="عنوان در url", unique=True)
    image = models.ImageField(upload_to='articles', verbose_name='تصویر')
    author = models.ForeignKey(User, verbose_name='نویسنده', on_delete=models.CASCADE)
    excerpt = models.TextField(verbose_name='گزیده')
    meta_description = models.CharField(max_length=500, verbose_name='توضیحات متا')
    content = RichTextField(verbose_name='متن مقاله')
    tag = models.ManyToManyField(ArticleTags, verbose_name='تگ ها', blank=True)
    reading_time = models.PositiveIntegerField(default=0, verbose_name='زمان مطالعه')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def save(self, *args, **kwargs):
        self.content = add_heading_ids(self.content)
        self.reading_time = calculate_reading_time(self.content)
        # self.created_at = to_shamsi(self.created_at)
        # self.updated_at = to_shamsi(self.updated_at)

        super().save(*args, **kwargs)

    # def get_jalali_date(self):
    #     return date2jalali(self.created_at)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

class ArticleVisit(models.Model):
    article = models.ForeignKey(ArticleModel, verbose_name='مقاله', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='کاربر')
    ip = models.GenericIPAddressField(verbose_name='IP')

    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name = 'تعداد بازدید'
        verbose_name_plural = 'تعداد بازدید ها'

class ArticleComments(models.Model):
    comment = models.TextField(verbose_name='کامنت')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE, verbose_name='مقاله')
    parent = models.ForeignKey('ArticleComments', null=True, blank=True, on_delete=models.CASCADE, verbose_name='والد')
    create_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ثبت')

    def __str__(self):
        return f'{self.article}: {self.comment}'

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    comment = models.ForeignKey(ArticleComments, on_delete=models.CASCADE, verbose_name='نظر')

    class Meta:
        unique_together = ('user', 'comment')
        verbose_name = 'لایک'
        verbose_name_plural = 'لایک ها'

    def __str__(self):
        return f'{self.user}: {self.comment}'