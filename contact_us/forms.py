from django import forms

from contact_us.models import ContactUsModel


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUsModel
        fields = ['full_name', 'email', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'نام و نام خانوادگی',
                    'oninvalid': 'this.setCustomValidity("لطفا نام و نام خانوادگی خود را وارد کنید")',
                    'oninput': 'this.setCustomValidity("")'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'ایمیل',
                    'oninvalid': 'this.setCustomValidity("لطفا ایمیل خود را وارد کنید")',
                    'oninput': 'this.setCustomValidity("")'
                }
            ),
            'subject': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'موضوع',
                    'oninvalid': 'this.setCustomValidity("لطفا موضوع را وارد کنید")',
                    'oninput': 'this.setCustomValidity("")'
                }
            ),
            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'متن پیام شما...',
                    'rows': 3,
                    'oninvalid': 'this.setCustomValidity("لطفا پیام خود را وارد کنید")',
                    'oninput': 'this.setCustomValidity("")'
                }
            )
        }