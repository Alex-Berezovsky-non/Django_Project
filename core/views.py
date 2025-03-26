from django.shortcuts import render
from .data import masters, services, orders  # ✅ Импорт из data.py

def landing(request):
    return render(request, 'landing.html', {
        'masters': masters,
        'services': services
    })

def thanks(request):
    return render(request, 'core/thanks.html')

def orders_list(request):
    return render(request, 'core/orders_list.html', {
        'orders': orders
    })

def order_detail(request, order_id):
    order = next((o for o in orders if o['id'] == order_id), None)
    
    if not order:  # ✅ Обработка отсутствия заявки
        return render(request, 'core/404.html', status=404)
    
    master = next((m for m in masters if m['id'] == order['master_id']), None)
    return render(request, 'core/order_detail.html', {
        'order': order,
        'master': master
    })
