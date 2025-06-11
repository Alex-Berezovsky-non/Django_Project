from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, F, Prefetch
from django.http import JsonResponse
from django.utils import timezone
from core.models import Master, Service, Order, Review
from core.forms import ReviewForm, OrderForm, ServiceForm, ServiceEasyForm
from core.mixins import StaffRequiredMixin
import logging

logger = logging.getLogger(__name__)

class LandingPageView(TemplateView):
    template_name = 'landing.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters'] = Master.objects.filter(is_active=True)
        context['reviews'] = Review.objects.filter(is_published=True)
        context['services'] = Service.objects.all()
        return context

class ThanksView(TemplateView):
    template_name = 'core/thanks.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['source'] = self.kwargs.get('source', 'general')
        return context

class OrdersListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Order
    template_name = 'core/orders_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date_created')

        search_query = self.request.GET.get('q', '')
        search_fields = self.request.GET.getlist('fields')
        status_filter = self.request.GET.get('status')
        date_from = self.request.GET.get('date_from')
        
        if search_query and search_fields:
            q_objects = Q()
            if 'client' in search_fields:
                q_objects |= Q(client_name__icontains=search_query)
            if 'phone' in search_fields:
                q_objects |= Q(phone__icontains=search_query)
            if 'comment' in search_fields:
                q_objects |= Q(comment__icontains=search_query)
            queryset = queryset.filter(q_objects)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if date_from:
            try:
                parsed_date = timezone.datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(appointment_date__gte=parsed_date)
            except (ValueError, TypeError):
                pass
                
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['search_fields'] = self.request.GET.getlist('fields')
        context['selected_status'] = self.request.GET.get('status')
        context['selected_date'] = self.request.GET.get('date_from')
        context['status_choices'] = Order.STATUS_CHOICES
        return context

class OrderDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Order
    template_name = 'core/order_detail.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'order'

class MasterDetailView(DetailView):
    model = Master
    template_name = 'core/master_detail.html'
    context_object_name = 'master'
    pk_url_kwarg = 'master_id'
    
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'services',
            Prefetch(
                'reviews',
                queryset=Review.objects.filter(is_published=True),
                to_attr='published_reviews'
            )
        )
    
    def get_object(self, queryset=None):
        master = super().get_object(queryset)
        
        Master.objects.filter(pk=master.pk).update(view_count=F('view_count') + 1)
        master.refresh_from_db()
        
        viewed_masters = self.request.session.get('viewed_masters', [])
        if master.id not in viewed_masters:
            viewed_masters.append(master.id)
            self.request.session['viewed_masters'] = viewed_masters
        
        return master
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        master = context['master']
        context['reviews'] = master.published_reviews
        context['services'] = master.services.all()
        context['title'] = f'Мастер: {master.name}'
        return context

class ServicesListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Service
    template_name = 'core/services_list.html'
    context_object_name = 'services'

class ServiceCreateView(StaffRequiredMixin, CreateView):
    model = Service
    template_name = 'core/service_create.html'
    fields = ['name', 'description', 'price', 'duration', 'is_popular', 'image']
    success_url = reverse_lazy('services_list')
    
    def get_form_class(self):
        form_mode = self.kwargs.get('form_mode', 'normal')
        return ServiceEasyForm if form_mode == 'easy' else ServiceForm
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Услуга успешно создана!')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при создании услуги')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Создание новой услуги'
        return context

class ServiceUpdateView(StaffRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'core/service_update.html'
    success_url = reverse_lazy('services_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Услуга успешно обновлена!')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при обновлении услуги')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Редактирование услуги: {self.object.name}'
        return context

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'core/order_create.html'
    success_url = reverse_lazy('landing')
    
    def get_success_url(self):
        return reverse_lazy('thanks', kwargs={'source': 'order'})
    
    def form_valid(self, form):
        form.instance.status = 'pending'
        response = super().form_valid(form)
        messages.success(
            self.request, 
            'Запись успешно создана! Мы свяжемся с вами для подтверждения.'
        )
        return response
    
    def form_invalid(self, form):
        messages.error(
            self.request, 
            'Пожалуйста, исправьте ошибки в форме'
        )
        return super().form_invalid(form)

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'core/review_form.html'
    
    def get_success_url(self):
        return reverse_lazy('thanks', kwargs={'source': 'review'})
    
    def get_initial(self):
        initial = super().get_initial()
        if 'master_id' in self.request.GET:
            initial['master'] = self.request.GET.get('master_id')
        return initial
    
    def form_valid(self, form):
        form.instance.is_published = False  
        response = super().form_valid(form)
        messages.success(self.request, 'Отзыв отправлен на модерацию!')
        return response

class MastersServicesAjaxView(View):
    def get(self, request, *args, **kwargs):
        master_id = request.GET.get('master_id')
        return self.get_services_json_response(master_id)
    
    def get_services_json_response(self, master_id):
        try:
            logger.info(f"Запрос услуг для мастера ID: {master_id}")
            master = Master.objects.get(pk=master_id, is_active=True)
            logger.info(f"Найден мастер: {master.name}")
            
            services = master.services.all()
            logger.info(f"Найдено услуг: {services.count()}")
            
            services_data = [{
                'id': service.id,
                'name': service.name,
                'price': str(service.price) 
            } for service in services]
            
            return JsonResponse({
                'services': services_data,
                'master_name': master.name
            })
        except Master.DoesNotExist:
            logger.error(f"Мастер с ID {master_id} не найден или не активен")
            return JsonResponse({
                'error': 'Мастер не найден или не активен'
            }, status=404)
        except ValueError:
            logger.error(f"Неверный формат ID мастера: {master_id}")
            return JsonResponse({
                'error': 'Неверный формат ID мастера'
            }, status=400)
        except Exception as e:
            logger.exception(f"Неожиданная ошибка: {str(e)}")
            return JsonResponse({
                'error': 'Внутренняя ошибка сервера'
            }, status=500)

class MasterInfoAjaxView(View):
    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            master_id = request.GET.get('master_id')
            return self.get_master_info(master_id)
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    def get_master_info(self, master_id):
        if not master_id:
            return JsonResponse({'error': 'Master ID is required'}, status=400)
        
        try:
            master = Master.objects.get(pk=master_id, is_active=True)
            data = {
                'name': master.name,
                'experience': master.experience,
                'photo': master.photo.url if master.photo else None,
                'services': [s.name for s in master.services.all()],
            }
            return JsonResponse(data)
        except Master.DoesNotExist:
            return JsonResponse({
                'error': 'Мастер не найден или не активен'
            }, status=404)