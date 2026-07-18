from random import randrange
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from iranian_cities.models import County

from user_module.forms import RegisterForm, VerificationForm, LoginForm, EditProfileModelForm, ChangePasswordForm, \
    AddressModelForm
from user_module.models import User, UserAddress
from django.contrib import messages

# Create your views here.

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'user_module/register.html', {'form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = User(
                first_name=register_form.cleaned_data['first_name'],
                last_name=register_form.cleaned_data['last_name'],
                username=register_form.cleaned_data['username'],
                phone_number=register_form.cleaned_data['phone_number'],
                email=register_form.cleaned_data['email'],
                active_phone_number=str(randrange(100000, 999999)),
                is_active=False,
            )
            user.set_password(register_form.cleaned_data['password'])
            user.save()
            request.session['user_id'] = user.id
            return redirect(reverse('verification_page'))

        print(register_form.errors)

        return render(request, 'user_module/register.html', {'form': register_form})


def verify_password(request):
    if request.method == 'GET':
        verify_ph = VerificationForm()
        print(request.session['user_id'])
        return render(request, 'user_module/verify_phone_number.html', {'verify_ph': verify_ph})

    if request.method == 'POST':
        verify_ph = VerificationForm(request.POST)
        if verify_ph.is_valid():
            user = User.objects.get(active_phone_number__iexact=verify_ph.cleaned_data['active_phone_number'],
                                    id=request.session['user_id'])
            if user:
                user.is_active = True
                user.save()
                return redirect(reverse('login_page'))
            raise ValidationError('کاربر موجود نیست')
        return render(request, 'user_module/verify_phone_number.html', {'verify_ph': verify_ph})


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'user_module/login_page.html', {
            'login_form': login_form,
        })

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name_email = login_form.cleaned_data['emailOrUsername']
            password = login_form.cleaned_data['password']
            user = User.objects.filter(Q(email__iexact=user_name_email) | Q(username__iexact=user_name_email)).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('emailOrUsername', 'حساب کاربری شما فعال نشده است!')

                else:
                    check_password = user.check_password(password)
                    if check_password:
                        login(request, user)
                        return redirect(reverse('home-page'))
                    else:
                        login_form.add_error('password', 'ایمیل یا نام کاربری یا رمز عبور اشتباه است')

            else:
                login_form.add_error('password', 'ایمیل یا نام کاربری یا رمز عبور اشتباه است')

        context = {
            'login_form': login_form,
        }
        return render(request, 'user_module/login_page.html', context)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        current_user = User.objects.get(id=request.user.id)
        edit_form = EditProfileModelForm(instance=current_user)
        address_user = UserAddress.objects.filter(user=current_user).first()
        if address_user:
            address_form = AddressModelForm(instance=address_user)
        else:
            address_form = AddressModelForm()
        change_pass_form = ChangePasswordForm()
        # address_form.fields['province'].queryset = Pro
        context = {
            'edit_form': edit_form,
            'change_pass_form': change_pass_form,
            'address_form': address_form,
        }
        return render(request, 'user_module/edit_profile.html', context)


class EditInfoView(View):

    def post(self, request):
        current_user = User.objects.get(id=request.user.id)
        edit_form = EditProfileModelForm(request.POST, instance=current_user)
        change_pass_form = ChangePasswordForm()
        address_user = UserAddress.objects.filter(user=current_user).first()
        if address_user:
            address_form = AddressModelForm(instance=address_user)
        else:
            address_form = AddressModelForm()

        if edit_form.is_valid():
            edit_form.save(commit=True)
            return redirect('profile_page')

        context = {
            'edit_form': edit_form,
            'change_pass_form': change_pass_form,
            'address_form': address_form,
            'active_tab': 'info'
        }
        return render(request, 'user_module/edit_profile.html', context)

class ChangePasswordView(View):

    def post(self, request):
        current_user = User.objects.get(id=request.user.id)
        edit_form = EditProfileModelForm(instance=current_user)
        change_pass_form = ChangePasswordForm(request.POST)
        address_user = UserAddress.objects.filter(user=current_user).first()
        if address_user:
            address_form = AddressModelForm(instance=address_user)
        else:
            address_form = AddressModelForm()
        if change_pass_form.is_valid():
            old_pass = change_pass_form.cleaned_data['old_password']
            check_pass = current_user.check_password(old_pass)
            if check_pass:
                new_pass = change_pass_form.cleaned_data['new_password']
                current_user.set_password(new_pass)
                current_user.save()
                update_session_auth_hash(request, current_user)
                messages.success(request, 'رمز شما با موفقیت تغییر یافت')
                return redirect('profile_page')
            else:
                change_pass_form.add_error('old_password', 'رمز عبور فعلی اشتباه است!')

        context = {
            'edit_form': edit_form,
            'change_pass_form': change_pass_form,
            'address_form': address_form,
            'active_tab': 'password',
        }
        return render(request, 'user_module/edit_profile.html', context)


class EditAddressView(View):
    def post(self, request):
        current_user = User.objects.get(id=request.user.id)
        edit_form = EditProfileModelForm(instance=current_user)
        change_pass_form = ChangePasswordForm()
        address_user = UserAddress.objects.filter(user=current_user).first()

        if address_user:
            address_form = AddressModelForm(request.POST, instance=address_user)
        else:
            address_form = AddressModelForm(request.POST)

        if address_form.is_valid():
            postal_code = address_form.cleaned_data['postal_code']
            if len(postal_code) == 10 and postal_code.isdigit():
                address = address_form.save(commit=False)
                address.user = current_user
                address.save()
                return redirect('profile_page')
            elif len(postal_code) != 10:
                address_form.add_error('postal_code', 'کد پستی باید 10 رقم باشد!')

            elif not postal_code.isdigit():
                address_form.add_error('postal_code', 'لطفا عدد وارد کنید!')

        context = {
            'edit_form': edit_form,
            'change_pass_form': change_pass_form,
            'address_form': address_form,
            'active_tab': 'address',
        }

        return render(request, 'user_module/edit_profile.html', context)


def load_counties(request):
    province_id = request.GET.get('province')
    counties = County.objects.filter(province_id=province_id)
    context = {
        'counties': counties,
    }
    return render(request, 'user_module/components/counties_partial.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))


