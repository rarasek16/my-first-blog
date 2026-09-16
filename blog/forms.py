from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "text",
            "category",
            "learning_goal",
            "code_example",
            "code_explanation",
            "practice_task",
        ]
        help_texts = {
            "learning_goal": "Jednou větou popiš, co se čtenář po lekci naučí.",
            "code_example": "Vkládej jen zdrojový kód bez formátování HTML.",
            "code_explanation": "Vysvětli, co dělají nejdůležitější řádky ukázky.",
            "practice_task": "Zadej samostatný úkol, kterým čtenář porozumění ověří.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["aria-describedby"] = f"{name}-help {name}-errors"


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["aria-describedby"] = f"{name}-help {name}-errors"
