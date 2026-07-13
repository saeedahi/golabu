from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from order_module.models import Order, OrderDetail
from products_module.models import Product

# Create your views here.

@login_required
def add_product_to_order(request):
    print(request.GET)
    product_id = request.GET.get('product_id')
    count = int(request.GET.get('count'))

    if count < 1:
        return JsonResponse(
            {
                'status': 'invalid_count'
            }
        )

    product = Product.objects.filter(id=product_id, is_active=True, is_available=True).first()
    if product:
        current_order = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)[0]
        current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
        if current_order_detail is not None:
            current_order_detail.count += int(count)
            current_order_detail.save()
        else:
            new_detail = OrderDetail.objects.create(product_id=product_id, count=count, order_id=current_order.id)
            new_detail.save()
        return JsonResponse({
            'status': 'success'
        })

    else:
        return JsonResponse({
            'status': 'not found'
        })


    return JsonResponse(
        {
            'status': ''
        }
    )


def user_basket(request):
    current_order = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)[0]
    total_amount = 0
    for order_detail in current_order.orderdetail_set.all():
        total_amount += order_detail.product.price * order_detail.count

    context = {
        'order': current_order,
        'sum': total_amount,
    }
    return render(request, 'order_module/cart.html', context)


def remove_order_detail(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found'
        })

    # current_order = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)[0]
    # detail = current_order.orderdetail_set.filter(id=detail_id).first()

    deleted_count, deleted_dict = OrderDetail.objects.filter(id=detail_id, order__is_paid=False, order__user_id=request.user.id).delete()

    if deleted_count == 0:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    # detail.delete()


    current_order = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)[0]
    total_amount = current_order.calculate_total_amount()

    context = {
        'order': current_order,
        'sum': total_amount,
    }

    data = render_to_string('order_module/includes/cart_content.html', context)

    return JsonResponse({
        'status': 'success',
        'data': data
    })


def change_order_detail_count(request):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found'
        })

    order_detail = OrderDetail.objects.filter(id=detail_id, order__is_paid=False, order__user_id=request.user.id).first()

    if order_detail is None:
        return JsonResponse({
            'status': 'not_found'
        })

    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.count = 1
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid'
        })

    current_order = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)[0]
    total_amount = current_order.calculate_total_amount()

    context = {
        'order': current_order,
        'sum': total_amount,
    }

    data = render_to_string('order_module/includes/cart_content.html', context)

    return JsonResponse({
        'status': 'success',
        'data': data
    })

