from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView

from products_module.models import Product, ProductCategory


# Create your views here.

class SearchListView(ListView):
    template_name = 'site_module/search_result.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        query = super(SearchListView, self).get_queryset()
        result = self.request.GET.get('q')
        if result:
            query = Product.objects.filter(
                Q(name__icontains=result) |
                Q(short_description__icontains=result) |
                Q(category__name__icontains=result) , is_active=True
            )
        else:
            # url_name = self.request.resolver_match.url_name
            # return redirect(url_name)
            return Product.objects.none()

        return query

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        context['result'] = self.request.GET.get('q')
        context['categories'] = ProductCategory.objects.all()
        return context