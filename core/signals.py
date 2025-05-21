from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings
from .models import Order
from .utils.telegram_bot import send_telegram_message

@receiver(m2m_changed, sender=Order.services.through)
def notify_order_with_services(sender, instance, action, **kwargs):
    if action == "post_add" and instance.id:
        services = instance.services.all()
        services_list = "\n".join([f"- {s.name}" for s in services])
        admin_url = reverse('admin:core_order_change', args=[instance.id])
        full_url = f"{settings.BASE_URL}{admin_url}"
        
        message = (
            "🎉 *Новая заявка!*\n"
            f"🔖 *ID:* {instance.id}\n"
            f"👤 *Имя:* {instance.client_name}\n"
            f"📞 *Телефон:* {instance.phone}\n"
            f"🗓 *Дата записи:* {instance.appointment_date.strftime('%d.%m.%Y %H:%M')}\n"
            f"📋 *Услуги:*\n{services_list}\n"
            f"🔗 [Ссылка на заявку]({full_url})"
        )
        
        send_telegram_message(
            settings.TELEGRAM_BOT_API_KEY,
            settings.TELEGRAM_USER_ID,
            message
        )