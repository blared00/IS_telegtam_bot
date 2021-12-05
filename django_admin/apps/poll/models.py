from django.db import models
from django.contrib.auth import get_user_model

from django_admin.apps.useradmin.models import Member


class Poll(models.Model):
    """Темы обучения."""

    title = models.CharField("Название", max_length=200)

    class Meta:
        verbose_name = "тему обучения"
        verbose_name_plural = "темы обучения"
        db_table = "polls"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Уроки."""

    DIFFICULTY = (
        (1, "Легкая"),
        (2, "Средняя"),
        (3, "Сложная"),
        (4, "Эксперт"),
    )
    title = models.CharField("Название", max_length=200)
    poll = models.ForeignKey(
        "Poll", on_delete=models.PROTECT, related_name="lesson", verbose_name="Тема"
    )
    difficulty = models.IntegerField("Сложность", choices=DIFFICULTY)

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"

    def __str__(self):
        return (
            self.title
            + " "
            + self.poll.title
            + " "
            + self.DIFFICULTY[self.difficulty - 1][1]
        )


class Question(models.Model):
    """Текст обучения."""

    lesson = models.ForeignKey(
        "Lesson",
        on_delete=models.PROTECT,
        related_name="question",
        verbose_name="Урок",
        null=True,
    )
    text = models.TextField("Текст вопроса", max_length=4096)
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
        verbose_name = "текст обучения"
        verbose_name_plural = "тексты обучения"
        ordering = ("add_date", "pk")

    def __str__(self):
        return self.text


class QuestionOptions(models.Model):
    """Варианты ответа для опроса."""

    count_key = models.PositiveSmallIntegerField("Количество кнопок")
    text_key = models.CharField(
        "Текст кнопок",
        max_length=256,
        help_text='Надписи кнопок записываются в строчку и разделяются ";"',
    )

    class Meta:
        verbose_name = "кнопки"
        verbose_name_plural = "кнопки"

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
    """Фиксация времени прохождения обучения."""

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
