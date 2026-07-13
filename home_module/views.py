from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from products_module.models import Product
from site_module.models import SiteSettings


# Create your views here.

class HomePageView(View):
    def get(self, request):
        products = Product.objects.all().filter(is_active=True, is_available=True)
        return render(request, 'home_module/home_page.html', {
            'products': products,
        })

def header_partial(request):
    context = {
        'main_setting': SiteSettings.objects.filter(is_main_setting=True).first(),
    }
    return render(request, 'site_header_partial.html',context)

def footer_partial(request):
    context = {
        'main_setting': SiteSettings.objects.filter(is_main_setting=True).first(),
    }
    return render(request, 'site_footer_partial.html', context)