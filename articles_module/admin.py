from django.contrib import admin
from . import models

class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category']
    list_editable = ['author', 'category']


class ArticleCommentsAdmin(admin.ModelAdmin):
    list_display = ['create_date']


admin.site.register(models.ArticleModel, ArticleModelAdmin)
admin.site.register(models.ArticleVisit)
admin.site.register(models.ArticleCategory)
admin.site.register(models.ArticleComments, ArticleCommentsAdmin)
admin.site.register(models.CommentLike)
admin.site.register(models.ArticleTags)