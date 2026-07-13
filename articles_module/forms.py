from django import forms
from django.forms import ModelForm
from articles_module import models


class ArticleCommentForm(ModelForm):
    class Meta:
        model = models.ArticleComments
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'id':'bpComment',
                    'rows' : 3,
                    'placeholder' : "نظر خود را بنویسید...",
                }
            )
        }