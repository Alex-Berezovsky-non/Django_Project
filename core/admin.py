from django.contrib import admin
from django.utils.html import format_html
from .models import Order, Master, Service, Review

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular')
    list_editable = ('is_popular',) 
    search_fields = ('name',)

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'experience', 'is_active')
    list_filter = ('is_active', 'experience')
    filter_horizontal = ('services',)
    search_fields = ('name', 'phone')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'phone', 'status_color', 'appointment_date', 'master')
    list_filter = ('status', 'master', 'appointment_date')
    filter_horizontal = ('services',)
    search_fields = ('client_name', 'phone', 'id')
    list_select_related = ('master',) 
    
    def status_color(self, obj):
        return format_html(
            '<span class="badge {}">{}</span>',
            obj.get_status_css_class(),
            obj.get_status_display()
        )
    status_color.short_description = 'Статус'
    status_color.admin_order_field = 'status' 

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'master', 'rating_stars', 'created_at', 'is_published')
    list_filter = ('is_published', 'rating', 'master')
    list_editable = ('is_published',)
    search_fields = ('client_name', 'text')
    date_hierarchy = 'created_at'
    actions = ['publish_reviews', 'unpublish_reviews']
    
    def rating_stars(self, obj):
        return format_html(
            '<span style="color: gold;">{}</span>',
            '★' * obj.rating + '☆' * (5 - obj.rating)
        )
    rating_stars.short_description = 'Рейтинг'
    
    def publish_reviews(self, request, queryset):
        queryset.update(is_published=True)
    publish_reviews.short_description = "Опубликовать выбранные отзывы"
    
    def unpublish_reviews(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_reviews.short_description = "Снять с публикации выбранные отзывы"
