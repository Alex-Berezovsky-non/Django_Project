from django.contrib import admin
from .models import Order, Master, Service, Review

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular')

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'experience', 'is_active')
    filter_horizontal = ('services',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone', 'status', 'appointment_date')
    list_filter = ('status', 'master')
    filter_horizontal = ('services',)
    search_fields = ('client_name', 'phone')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'master', 'rating', 'is_published')
    list_filter = ('rating', 'is_published')
# Register your models here.
