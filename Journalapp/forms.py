'''
FORMS of JOURNAL
'''
from django import forms
from .models import Journal
from tinymce.widgets import TinyMCE

class JournalForm(forms.ModelForm):
    long_term_goal = forms.BooleanField(
        required=False,
        label="Is this a Long-Term Goal?",
    )
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Due Date",
    )

    password = forms.CharField(
        max_length=128,
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Optional Password'}),
        help_text="Set a password to protect this entry."
    )

    class Meta:
        model = Journal
        fields = ['title', 'content', 'password', 'long_term_goal', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter journal title'}),
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 15}),  # Default to textarea
        }
