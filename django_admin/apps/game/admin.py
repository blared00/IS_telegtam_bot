from django.contrib import admin
from django.utils.safestring import mark_safe

from django_admin.apps.game.models import Question, QuestionOptions, QuestionCategory, MemberCategoryScore


class QuestionOptionsAdmin(admin.TabularInline):
    """Варианты ответов на вопросы"""
    model = QuestionOptions


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Вопросы"""
    list_display = ('text', 'category', 'difficulty', 'owner', 'ispicture', 'is_active')
    inlines = (QuestionOptionsAdmin, )
    readonly_fields = ('get_picture', )
    exclude = ('owner', 'cash')
    list_filter = ('category',)

    ordering = ('-is_active', 'add_date',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.cash = None
        super().save_model(request, obj, form, change)

    @admin.display(boolean=True, description='Изображение')
    def ispicture(self, obj):
        if obj.picture:
            return True
        return False

    @admin.display(description='Превью')
    def get_picture(self, obj):
        if obj.picture:
            return mark_safe(f'<img src="{obj.picture.url}" style="max-width:600px;width:100%">')
        return ''


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    """Отображение категорий вопросов в панели администратора."""
    pass


@admin.register(MemberCategoryScore)
class QMemberCategoryScoreAdmin(admin.ModelAdmin):
    """Отображение баллов пользователей в панели администратора."""
    list_display = ('member', 'category', 'amount')
    list_filter = ('category', )
