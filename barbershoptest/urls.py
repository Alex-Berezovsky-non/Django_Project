from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('thanks/', views.thanks, name='thanks'),
    path('orders/', login_required(views.orders_list), name='orders_list'),
    path('orders/<int:pk>/', login_required(views.order_detail), name='order_detail'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('review/create/', views.create_review, name='create_review'),
    path('api/master-info/', views.get_master_info, name='get_master_info'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)