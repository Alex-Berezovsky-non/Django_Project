from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('thanks/', views.thanks, name='thanks'),
    path('orders/', 
         login_required(views.orders_list), 
         name='orders_list'),
    
    path('orders/<int:pk>/', 
         login_required(views.order_detail), 
         name='order_detail'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    ) 