from django.db import models
from django.contrib.auth import get_user_model

from django_admin.apps.useradmin.models import Member


class Poll(models.Model):
    """Темы тестов."""
    title = models.CharField("Название", max_length=200)

    class Meta:
        verbose_name = "Темы тестов"
        verbose_name_plural = "Темы тестов"
        db_table = "polls"

    def __str__(self):
        return self.title


class Question(models.Model):
    """Вопросы для опроса."""

    poll = models.ForeignKey(
        "Poll", on_delete=models.PROTECT, related_name="question", verbose_name="Опрос"
    )
    text = models.TextField("Текст вопроса", max_length=4096)
    text_answer = models.BooleanField(verbose_name="Возможен ответ текстом?")
    options = models.ForeignKey(
        "QuestionOptions", on_delete=models.PROTECT, verbose_name="Варианты ответа"
    )
    add_date = models.DateTimeField("Дата создания", auto_now_add=True)
    update_date = models.DateTimeField("Дата изменения", auto_now=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Создатель",
        default=1,
        related_name="poll_question",
    )

    class Meta:
        verbose_name = "вопрос к опросу"
        verbose_name_plural = "вопросы"
        ordering = ("add_date", "pk")

    def __str__(self):
        return self.text + f" (Опрос - {str(self.poll.pk)}"


class QuestionOptions(models.Model):
    """Варианты ответа для опроса."""

    count_key = models.PositiveSmallIntegerField("Количество кнопок")
    text_key = models.CharField(
        "Текст кнопок",
        max_length=256,
        help_text='Надписи кнопок записываются в строчку и разделяются ";"',
    )

    class Meta:
        verbose_name = "кнопки ответов"
        verbose_name_plural = "кнопки ответов"

    def __str__(self):
        return f"{'| '.join(self.text_key.split(';'))}"


class QuestionAnswer(models.Model):
    """Ответы пользователей на вопросы"""

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="pquestion_answer",
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="Вопрос",
        related_name="pquestion_answer",
    )
    answer = models.CharField("Ответ", max_length=256)
    date = models.DateTimeField("Дата ответа", auto_now_add=True)

    class Meta:
        verbose_name = "ответ к вопросу"
        verbose_name_plural = "ответы к вопросам"

    def __str__(self):
        return str(self.member.tg_id) + f"на вопрос({self.question.pk})"


class Answer(models.Model):
    """Фиксация времени прохождения опроса пользователем."""

    poll = models.ForeignKey(
        Poll, on_delete=models.PROTECT, verbose_name="Опрос", related_name="poll_answer"
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="poll_answer",
    )
    date = models.DateTimeField("Дата ответа", auto_now_add=True)

    class Meta:
        verbose_name = "результаты тестирования"
        verbose_name_plural = "результаты тестирования"

    def __str__(self):
        return f"""Опрос:{self.poll.pk},
               пользователь: {self.member.name}, 
               дата: {self.date.strftime('%d.%m.%y %H:%M')}"""


