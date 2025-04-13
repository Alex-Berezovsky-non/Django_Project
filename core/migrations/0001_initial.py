# Generated by Django 5.1.7 on 2025-04-13 20:01

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('photo', models.ImageField(blank=True, upload_to='masters/', verbose_name='Фотография')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('experience', models.PositiveIntegerField(help_text='Опыт работы в годах', verbose_name='Стаж работы')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
            ],
            options={
                'verbose_name': 'Мастер',
                'verbose_name_plural': 'Мастера',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('duration', models.PositiveIntegerField(help_text='Время выполнения в минутах', verbose_name='Длительность')),
                ('is_popular', models.BooleanField(default=False, verbose_name='Популярная услуга')),
                ('image', models.ImageField(blank=True, upload_to='services/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('client_name', models.CharField(blank=True, max_length=100, verbose_name='Имя клиента')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='reviews/', verbose_name='Фотография')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликован')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.master', verbose_name='Мастер')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('client_name', models.CharField(max_length=100, verbose_name='Имя клиента')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('status', models.CharField(choices=[('not_approved', 'Не подтвержден'), ('approved', 'Подтвержден'), ('completed', 'Выполнен'), ('canceled', 'Отменен')], default='not_approved', max_length=50, verbose_name='Статус')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('appointment_date', models.DateTimeField(verbose_name='Дата и время записи')),
                ('master', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.master', verbose_name='Мастер')),
                ('services', models.ManyToManyField(related_name='orders', to='core.service', verbose_name='Услуги')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.AddField(
            model_name='master',
            name='services',
            field=models.ManyToManyField(related_name='masters', to='core.service', verbose_name='Услуги'),
        ),
    ]
