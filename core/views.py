from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Master, Service, Order, Review
from django.db.models import Q

def landing(request):
    masters = Master.objects.filter(is_active=True)
    reviews = Review.objects.filter(is_published=True)
    services = Service.objects.all()  # Добавлено
    return render(request, 'landing.html', {
        'masters': masters,
        'reviews': reviews,
        'services': services 
    })

@login_required
def orders_list(request):
    search_query = request.GET.get('q', '')
    search_fields = request.GET.getlist('fields')

    orders = Order.objects.all().order_by('-date_created')
    
    if search_query and search_fields:
        q_objects = Q()
        if 'client' in search_fields:
            q_objects |= Q(client_name__icontains=search_query)
        if 'phone' in search_fields:
            q_objects |= Q(phone__icontains=search_query)
        if 'comment' in search_fields:
            q_objects |= Q(comment__icontains=search_query)
        
        orders = orders.filter(q_objects)

    return render(request, 'core/orders_list.html', {
        'orders': orders,
        'search_query': search_query,
        'search_fields': search_fields
    })

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'core/order_detail.html', {'order': order})

def thanks(request):
    """Страница благодарности после успешного создания заказа"""
    return render(request, 'core/thanks.html')
