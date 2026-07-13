from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from contact_us.forms import ContactUsForm
from site_module.models import SiteSettings
from user_module.models import User


# Create your views here.


class ContactUsView(View):
    def get(self, request):
        contact_form = ContactUsForm()
        site_settings = SiteSettings.objects.get(is_main_setting=True)
        context = {
            'site_settings': site_settings,
            'contact_form': contact_form,
        }
        return render(request, 'contact_us/contact_us_page.html', context)

    def post(self, request):
        contact_form = ContactUsForm(request.POST)
        site_settings = SiteSettings.objects.get(is_main_setting=True)
        if contact_form.is_valid():
            new_message = contact_form.save(commit=False)
            user = User.objects.filter(id=request.user.id).first()
            if user:
                new_message.user_id = user.id
            new_message.save()

        context = {
            'site_settings': site_settings,
            'contact_form': contact_form,
        }
        return redirect(reverse('contact_us_page'))