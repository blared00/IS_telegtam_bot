from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _

from django_admin.apps.useradmin.models import CustomUser


class CustomUserForm(UserChangeForm):
    telegram_id = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'vTextField'})
    )


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification.asdas"),
    )

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

