from django import forms
from django.forms import ModelForm
from products_module.models import ProductComment


class ProductCommentForm(ModelForm):
    class Meta:
        model = ProductComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'id':'product-comment',
                    'rows':3,
                    'placeholder': "نظر خود را بنویسید...",
                }
            )
        }