from django.contrib.auth import get_user_model
from django.db import models
from django_admin.apps.poll.models import Member


class MemberQuestion(models.Model):
    """Вопросы пользователей заданные в разделе помощи."""

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="help_question",
    )
    text = models.TextField("Вопрос", max_length=1900)
    date = models.DateTimeField("Дата ответа", auto_now=True)

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы пользователей"

    def __str__(self):
        return self.text


class AnswerOperator(models.Model):
    """Ответ оператора/модератора на вопрос"""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Оператор",
        default=1,
        related_name="help_question_answer",
    )
    question = models.OneToOneField(
        MemberQuestion, on_delete=models.CASCADE, verbose_name="Вопрос"
    )
    text = models.TextField("Ответ",
                            null=True,
                            max_length=1900,
                            help_text="Максимальное количество символов в ответе 1900")
    date_create = models.DateTimeField("Дата вопроса", auto_now_add=True)
    date_update = models.DateTimeField("Дата ответа", auto_now=True)

    class Meta:
        verbose_name = "ответ"
        verbose_name_plural = "вопросы пользователей"

    def __str__(self):
        return f"""Вопрос: {self.question.text}"""


class PinMessage(models.Model):
    """Закрепленное сообщение"""
    text = models.TextField(
        "Текст сообщения",
        help_text="Для отображения ссылок в сообщении воспользуйтесь конструкцией [текст](ссылка)",
        max_length=4096
    )

    class Meta:
        verbose_name = "закрепленное сообщение"
        verbose_name_plural = "закрепленное сообщение"

    def __str__(self):
        return f"Закрепленное сообщение (№{self.pk})"


class Newsletter(models.Model):
    """Рассылка сообщения пользователям"""
    text = models.TextField("Текст сообщения",
                            help_text="Для отображения ссылок в сообщении воспользуйтесь конструкцией [текст](ссылка)",
                            max_length=4096)
    date_create = models.DateTimeField("Дата рассылки", auto_now_add=True)
    picture = models.ImageField(
        "Изображение",
        upload_to="newsletter/%Y/%m/%d",
        null=True,
        blank=True,
        default=None,
        max_length=1024,
    )
    cash = models.CharField("Кэш фото", max_length=128, null=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        verbose_name="Оператор",
        related_name="newsletter",
    )

    class Meta:
        verbose_name = "новое сообщение"
        verbose_name_plural = "Рассылка сообщений"

    def __str__(self):
        return f"{self.text}"
