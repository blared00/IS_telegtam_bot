from django.apps import AppConfig


class PollConfig(AppConfig):
    """Настройки для приложения "Опросы" """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_admin.apps.poll'
    verbose_name = 'Обучение'
