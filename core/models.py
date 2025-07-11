from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(
        verbose_name="Длительность",
        help_text="Время выполнения в минутах"
    )
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    image = models.ImageField(upload_to="services/", blank=True, null=True, verbose_name="Изображение")

    def __str__(self):          
        return str(self.name)   

    class Meta:                 
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        indexes = [
            models.Index(fields=['is_popular']),          
            models.Index(fields=['price']),               
        ]

class Master(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя")
    photo = models.ImageField(
        upload_to="masters/", 
        default='masters/default_master.jpg', 
        blank=True, 
        null=True, 
        verbose_name="Фотография"
    )
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    experience = models.PositiveIntegerField(
        verbose_name="Стаж работы", 
        help_text="Опыт работы в годах"
    )
    services = models.ManyToManyField(
        Service, 
        related_name="masters", 
        verbose_name="Услуги"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    view_count = models.PositiveIntegerField(
        default=0, 
        verbose_name="Количество просмотров",
        help_text="Сколько раз просмотрена страница мастера"
    )

    def __str__(self):          
        return str(self.name)   
    
    def get_reviews(self):
        """Возвращает опубликованные отзывы о мастере"""
        return self.reviews.filter(is_published=True)

    class Meta:                 
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"
        indexes = [
            models.Index(fields=['is_active']),
        ]

class Order(models.Model):
    STATUS_NOT_APPROVED = 'not_approved'
    STATUS_APPROVED = 'approved'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELED = 'canceled'

    STATUS_CHOICES = [
        (STATUS_NOT_APPROVED, 'Не подтвержден'),
        (STATUS_APPROVED, 'Подтвержден'),
        (STATUS_COMPLETED, 'Выполнен'),
        (STATUS_CANCELED, 'Отменен'),
    ]

    STATUS_CSS_CLASSES = {
        STATUS_NOT_APPROVED: 'bg-warning',
        STATUS_APPROVED: 'bg-info',
        STATUS_COMPLETED: 'bg-success',
        STATUS_CANCELED: 'bg-danger',
    }

    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_NOT_APPROVED, 
        verbose_name="Статус"
    )
    id = models.AutoField(primary_key=True, verbose_name="ID")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    master = models.ForeignKey(
        Master,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Мастер"
    )
    services = models.ManyToManyField(
        Service, 
        related_name="orders",
        verbose_name="Услуги"
    )
    appointment_date = models.DateTimeField(verbose_name="Дата и время записи")

    def __str__(self):
        return f"Заказ #{self.id} - {self.client_name}"

    def get_status_css_class(self):
        return self.STATUS_CSS_CLASSES.get(self.status, 'bg-secondary')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-date_created'] 
        indexes = [
            models.Index(fields=['status', '-date_created']),
            models.Index(fields=['appointment_date']),
        ]

class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    client_name = models.CharField(max_length=100, blank=True, verbose_name="Имя клиента")
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        verbose_name="Мастер",
        related_name="reviews",
    )
    photo = models.ImageField(
        upload_to="reviews/", 
        blank=True, 
        null=True, 
        verbose_name="Фотография"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата создания"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )
    is_published = models.BooleanField(
        default=True, 
        verbose_name="Опубликован",
        help_text="Отображать ли отзыв на сайте"
    )
    
    def __str__(self):
        return f"Отзыв от {self.client_name}"
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_published', 'rating']),
            models.Index(fields=['created_at']),
        ]