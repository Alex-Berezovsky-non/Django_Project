from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from core import views as core_views

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),
    
    # Основные URL приложения core
    path('', core_views.LandingPageView.as_view(), name='landing'),
    path('thanks/<str:source>/', core_views.ThanksView.as_view(), name='thanks'),
    
    # Защищенные URL (требуют аутентификации и staff-статуса)
    path('orders/', login_required(core_views.OrdersListView.as_view()), name='orders_list'),
    path('orders/<int:pk>/', login_required(core_views.OrderDetailView.as_view()), name='order_detail'),
    path('services/', login_required(core_views.ServicesListView.as_view()), name='services_list'),
    
    # URL для мастеров
    path('master/<int:master_id>/', core_views.MasterDetailView.as_view(), name='master_detail'),
    
    # URL для работы с услугами
    path('services/create/', core_views.ServiceCreateView.as_view(), name='service_create'),
    path('services/update/<int:pk>/', core_views.ServiceUpdateView.as_view(), name='service_update'),
    
    # URL для создания заказа и отзыва
    path('order/create/', core_views.OrderCreateView.as_view(), name='order_create'),
    path('review/create/', core_views.ReviewCreateView.as_view(), name='create_review'),
    
    # AJAX API
    path('api/master-services/', core_views.MastersServicesAjaxView.as_view(), name='master_services'),
    path('api/master-info/', core_views.MasterInfoAjaxView.as_view(), name='get_master_info'),
    
    # Подключаем URL из приложения users с пространством имён 'users'
    path('users/', include('users.urls', namespace='users')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)