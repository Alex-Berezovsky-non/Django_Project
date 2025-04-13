from django.db import models
from django.core.validators import MinLengthValidator,MaxLengthValidator

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(
        verbose_name="Длительность",
        help_text="Время выполнения в минутах"
    )
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    image = models.ImageField(upload_to="services/", blank=True, verbose_name="Изображение")

    def __str__(self):          
        return str(self.name)   

    class Meta:                 
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

