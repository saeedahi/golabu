from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products_list_page'),
    path('add-comment/', views.addComment, name='add_product_comment'),
    path('like/', views.likeComment, name='add_like'),
    path('<str:slug>/', views.ProductDetailView.as_view(), name='product_detail_page'),
]