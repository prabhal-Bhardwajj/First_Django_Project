'''
TODOAPP forms.py
'''

from django import forms
from .models import LongTermGoal,Todo

from django import forms
from .models import LongTermGoal, Todo

class LongTermGoalForm(forms.ModelForm):
    class Meta:
        model = LongTermGoal
        fields = ['title', 'description', 'due_date', 'priority']

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'details', 'context', 'time', 'date', 'due_date', 'is_long_term_goal', 'priority']

