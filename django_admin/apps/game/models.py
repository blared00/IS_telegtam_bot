from django.contrib.auth import get_user_model
from django.core.validators import validate_image_file_extension, FileExtensionValidator
from django.db import models

from django_admin.apps.poll.models import Member


class QuestionCategory(models.Model):
    """Категории вопросов."""
    title = models.CharField("Название", max_length=32)

    class Meta:
        verbose_name = "категорию вопросов"
        verbose_name_plural = "категории вопросов"
        ordering = ("title",)

    def __str__(self):
        return self.title

class Question(models.Model):
    """Вопросы для интерактива."""
    DIFFICULTY = (
        (1, 'Легкая'),
        (2, 'Средняя'),
        (3, 'Сложная'),
        (4, 'Эксперт'),
    )

    text = models.TextField("Текст вопроса", max_length=4096)
    descriptions = models.TextField("Пояснение по вопросу", max_length=4000, null=True)
    add_date = models.DateTimeField("Дата создания", auto_now_add=True)
    update_date = models.DateTimeField("Дата изменения", auto_now=True)
    cash = models.CharField("Кэш фото", max_length=128, null=True)
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, verbose_name='Тема теста', related_name='question', null=True)
    difficulty = models.IntegerField('Сложность', choices=DIFFICULTY)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Создатель",
        default=1,
        related_name="game_question",
    )
    is_active = models.BooleanField('Активный', default=True)
    picture = models.ImageField(
        "Изображение",
        upload_to="game_picture/%Y/%m/%d",
        null=True,
        blank=True,
        default=None,
        max_length=1024,
        validators=(FileExtensionValidator(['jpg', 'jpeg', 'png']),)
    )

    class Meta:
        verbose_name = "вопрос к обучению"
        verbose_name_plural = "вопросы к обучению"
        ordering = ("add_date",)

    def __str__(self):
        return self.text


class QuestionOptions(models.Model):
    """Варианты ответа для вопроса"""

    text = models.CharField("Текст варианта", max_length=64)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name="Вопрос", related_name="option"
    )
    true_answer = models.BooleanField("Верный ответ?")

    class Meta:
        verbose_name = "варианты ответов"
        verbose_name_plural = "варианты ответов"

    def __str__(self):
        return self.text + f"({self.question.pk})"


class Answer(models.Model):
    """Ответы пользователей на вопросы интерактива"""

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="gquestion_answer",
    )
    option = models.ForeignKey(
        QuestionOptions, on_delete=models.CASCADE, verbose_name="Ответ"
    )
    date = models.DateTimeField("Дата ответа", auto_now_add=True)

    class Meta:
        verbose_name = "ответ на вопрос"
        verbose_name_plural = "ответы на вопросы"

    def __str__(self):
        return f"""Вопрос:{self.option.question.pk},
                   пользователь: {self.member.name}, 
                   дата: {self.date.strftime('%d.%m.%y %H:%M')}"""


class MemberCategoryScore(models.Model):
    """Количество баллов пользователя по теме."""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="Пользователь", related_name='score')
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, verbose_name='Тема теста', related_name='score')
    amount = models.IntegerField('Количество баллов', default=0)

    class Meta:
        verbose_name = "Баллы пользователей"
        verbose_name_plural = "Баллы пользователей"
        db_table = "member_score"

    def __str__(self):
        return f"Баллы пользователя: {self.member.name}"
