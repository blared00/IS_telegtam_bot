from django.contrib.auth.models import AbstractUser, UserManager, Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """Создание пользователя с True в разделе "Статус Персонала". """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Модель администратора."""
    email = models.EmailField(_('email address'), blank=True, null=True)
    telegram_id = models.IntegerField("Телеграм ID", null=True, blank=True, )
    on_vacation = models.BooleanField("В отпуске", default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=True,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    objects = CustomUserManager()

    class Meta:
        verbose_name = "администратора бота"
        verbose_name_plural = "администраторы бота"
        db_table = "user_admin"


class Member(models.Model):
    """Модель пользователя."""
    tg_id = models.PositiveIntegerField("Телеграм ID", primary_key=True)
    tg_name = models.CharField("Имя пользователя в Телеграм", max_length=32, null=True)
    name = models.CharField("Имя", max_length=64)

    class Meta:
        verbose_name = "пользователя бота"
        verbose_name_plural = "пользователи бота"
        db_table = "member"

    def __str__(self):
        return f"{self.tg_id}: {self.tg_name} - {self.name}"


class MemberState(models.Model):
    """Состояние пользователя."""
    member = models.OneToOneField(Member, on_delete=models.CASCADE, verbose_name="Пользователь", primary_key=True)
    main_message_id = models.PositiveIntegerField("id основного сообщения")
    pin_message_id = models.PositiveIntegerField("id закрепленного сообщения", null=True, blank=True)
    state = models.CharField("Положение пользователя", max_length=32, default=None, null=True, blank=True)

    class Meta:
        verbose_name = "состояние пользователя бота "
        verbose_name_plural = "состояния пользователей бота"
        db_table = "member_state"

    def __str__(self):
        return f"Состояние пользователя: {self.member.name}"


class CustomGroup(Group):
    class Meta:
        verbose_name = "группу прав доступа"
        verbose_name_plural = "группы прав доступа"
        db_table = "useradmin_group"
