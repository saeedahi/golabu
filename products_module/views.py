from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from products_module.forms import ProductCommentForm
from products_module.models import Product, ProductCategory, ProductComment, LikeComment, ProductSpecifications


# Create your views here.


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products_module/products_list.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category = self.request.GET.get('category')
        sort = self.request.GET.get('sort')
        if category:
            query = query.all().order_by('brand').filter(category__slug=category, is_active=True)

        if not sort:
            return query
        elif sort == "price-low":
            query = query.all().filter(is_active=True).order_by('price')
        elif sort == "price-high":
            query = query.all().order_by('-price')
        elif sort == "name":
            query = query.all().order_by('name')
        # elif sort == "most-view":
        #     query = query.order_by()
        return query

# def product_detail(request, slug):
#     product = Product.objects.get(slug__iexact=slug)
#     context = {
#         'product': product,
#     }
#     return render(request, 'products_module/product_detail.html', context)

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products_module/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = self.object
        context['comments'] = ProductComment.objects.filter(product_id=product.id, parent=None).order_by('-created_at').prefetch_related('productcomment_set')
        context['comment_form'] = ProductCommentForm()
        context['specifications'] = ProductSpecifications.objects.filter(product=product)
        return context

@login_required
def addComment(request):
    if request.method == 'POST':
        form = ProductCommentForm(request.POST)
        product_id = request.POST.get('product_id')
        parent_id = request.POST.get('parent_id')
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user_id = request.user.id
            new_comment.product_id = product_id
            if parent_id:
                new_comment.parent_id = parent_id

            new_comment.save()
        context = {
            'comments': ProductComment.objects.filter(product_id=product_id, parent=None).order_by('-created_at').prefetch_related('productcomment_set'),
            'comment_form': form
        }

        return render(request, 'products_module/includes/product_comment_partial.html', context)

@login_required
def likeComment(request):
    if request.method == 'POST':
        like_user_id = request.user.id
        comment = get_object_or_404(ProductComment, pk=request.POST.get('comment_id'))
        like = LikeComment.objects.filter(user_id=like_user_id, comment_id=comment.id).first()
        if like:
            like.delete()
        else:
            LikeComment.objects.create(user_id=like_user_id, comment_id=comment.id)

        return JsonResponse({
            'count': comment.likecomment_set.count(),
        })
