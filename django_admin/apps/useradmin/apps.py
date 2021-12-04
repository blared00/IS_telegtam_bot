from django.apps import AppConfig


class UserAdminConfig(AppConfig):
    """Настройки для приложения "Администраторы" """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_admin.apps.useradmin'
    verbose_name = 'Пользователи'

