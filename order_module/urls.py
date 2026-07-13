from django.urls import path
from order_module import views


urlpatterns = [
    path('add-to-order/', views.add_product_to_order, name='add_product_to_order_page'),
    path('cart/', views.user_basket, name='cart_page'),
    path('cart/remove-order-detail/', views.remove_order_detail, name='remove_order_detail_ajax'),
    path('cart/change-order-count/', views.change_order_detail_count, name='change_order_detail_count_ajax'),
]