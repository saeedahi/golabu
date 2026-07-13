from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.core.exceptions import ValidationError
from iranian_cities.models import Province, County

from user_module.models import User, UserAddress


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        label='نام',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام'
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    last_name = forms.CharField(
        label='نام خانوادگی',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام خانوادگی'
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    phone_number = forms.CharField(
        label='شماره موبایل',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'شماره موبایل'
        }),
        validators=[
            validators.MaxLengthValidator(10),
            validators.RegexValidator(regex=r'^[0-9]{10}$', message='شماره وارد شده معتبر نمیباشد'),
            # فقط اعداد 11 رقمی برای تلفن قبول است
        ]
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل'
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ]
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور'
        }),
        validators=[
            validators.MinLengthValidator(8),
            validators.RegexValidator(regex=r'[a-zA-z0-9]$', message='رمز عبور ایمن نیست')
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'تکرار رمز عبور'
        }),
        validators=[
            validators.MinLengthValidator(8),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password == confirm_password:
            return confirm_password

        raise ValidationError('رمز عبور و تکرار رمز عبور مغایرت دارند')

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number__iexact=phone_number).exists():
            raise ValidationError("این شماره قبلا ثبت شده است")

        return phone_number

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("این ایمیل قبلا ثبت شده است")

        return email


class LoginForm(forms.Form):
    emailOrUsername = forms.CharField(
        label="ایمیل یا نام کاربری",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )


class VerificationForm(forms.Form):
    active_phone_number = forms.CharField(
        label='کد تایید',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'کد تایید'
        }),
        validators=[
            validators.RegexValidator(regex=r'^[0-9]{6}$', )
        ]
    )


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'نام',
                    'autofocus': True,
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'نام خانوادگی',
                    'autofocus': True,
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'نام کاربری',
                    'autofocus': True,
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'ایمیل',
                    'autofocus': True,
                }
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'تلفن همراه',
                    'autofocus': True,
                }
            )
        }

        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'username': 'نام کاربری',
            'email': 'ایمیل',
            'phone_number': 'تلفن همراه',
        }

    def __init__(self, *args, **kwargs):
        super(EditProfileModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='رمز عبور فعلی',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور فعلی را وارد کنید'
        })
    )
    new_password = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'id': 'password',
            'class': 'form-control',
            'placeholder': 'رمز عبور جدید را وارد کنید'
        })
    )
    new_password_confirm = forms.CharField(
        label='تکرار رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'id': 'confirm_password',
            'class': 'form-control',
            'placeholder': 'رمز عبور جدید را مجدداً وارد کنید'
        })
    )

    def clean_new_password(self):
        new_password = self.cleaned_data['new_password']
        validate_password(new_password)
        return new_password

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("new_password")
        confirm = cleaned_data.get("new_password_confirm")

        if password and confirm and password != confirm:
            raise ValidationError("رمزهای عبور با هم مطابقت ندارند.")

        return cleaned_data


class AddressModelForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        exclude = ['user']
        widgets = {
            'province': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'province',
                    'name': 'province',
                }
            ),
            'county': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'county',
                    'name': 'county',
                }
            ),
            'district': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'محله / شهرک',
                }
            ),
            'street': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'خیابان / کوچه'
                }
            ),
            'building': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'نام ساختمان / مجتمع'
                }
            ),
            'number_plate': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'شماره پلاک'
                }
            ),
            'postal_code': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'کد پستی'
                }
            ),
            'full_address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'آدرس کامل',
                }
            )
        }

        labels = {
            'district': 'محله / شهرک',
            'street': 'خیابان / کوچه',
            'building': 'نام ساختمان / مجتمع',
            'number_plate': 'شماره پلاک',
            'postal_code': 'کد پستی',
            'full_address': 'آدرس کامل',
        }

    def __init__(self, *args, **kwargs):
        super(AddressModelForm, self).__init__(*args, **kwargs)
        self.fields['province'].queryset = Province.objects.all()
        self.fields['county'].queryset = County.objects.none()

        if "province" in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['county'].queryset = County.objects.filter(province_id=province_id)
            except:
                pass

        elif self.instance.pk:
            self.fields['county'].queryset = County.objects.filter(
                province_id=self.instance.province_id
            )
