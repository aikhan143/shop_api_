from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Указываем имя проекта Django и устанавливаем переменную окружения "DJANGO_SETTINGS_MODULE"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаем экземпляр Celery
app = Celery('config')

# Загружаем конфигурацию из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем и регистрируем задачи из файлов tasks.py приложений Django
app.autodiscover_tasks()