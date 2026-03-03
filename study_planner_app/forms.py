from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudyTask, Subject


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class StudyTaskForm(forms.ModelForm):
    due_date = forms.DateField(
        required=False,
        input_formats=["%Y-%m-%d", "%Y.%m.%d"],  # accept both 2026-03-03 and 2026.03.03
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date", "placeholder": "YYYY-MM-DD"},
        ),
    )

    class Meta:
            model = StudyTask
            fields = ("title", "description", "subject", "tags", "due_date", "priority", "status")


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ("name", "description")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Subject Name"}),
            "description": forms.Textarea(attrs={ "placeholder": "Description"}),
        }