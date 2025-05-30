import sys
import os
import django
from django.core.management import call_command

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershoptest.settings')
django.setup()

def main():
    with open('db_dump.json', 'w', encoding='utf-8') as f:
        # Сохраняем оригинальный stdout
        original_stdout = sys.stdout
        
        # Перенаправляем stdout в файл
        sys.stdout = f
        
        # Вызываем команду dumpdata
        call_command('dumpdata', indent=2)
        
        # Восстанавливаем stdout
        sys.stdout = original_stdout

if __name__ == '__main__':
    main()