from django import forms

from django_admin.apps.poll.models import Question


class QuestionForm(forms.ModelForm):
    text = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'class': 'vTextField;', 'size': '100'}))

    class Meta:
        model = Question
        fields = '__all__'
