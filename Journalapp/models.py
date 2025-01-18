'''
MODELS OF JOURNAL
'''
from django.db import models
from todoapp.models import LongTermGoal
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

class JournalCategory(models.TextChoices):
    PERSONAL = 'Personal', _('Personal')
    INFORMATION = 'Information', _('Information')
    THOUGHTS = 'Thoughts', _('Thoughts')
    TASKS = 'Tasks', _('Tasks')
    NOTES = 'Notes', _('Notes')
    NEWS = 'News', _('News')
    RANDOM = 'Random', _('Random')
    WORK = 'Work', _('Work')
    STUDY = 'Study', _('Study')
    FINANCE = 'Finance', _('Finance')
    TRAVEL = 'Travel', _('Travel')
    RECIPES = 'Recipes', _('Recipes')
    PROJECTS = 'Projects', _('Projects')
    IDEAS = 'Ideas', _('Ideas')
    HEALTH = 'Health', _('Health')
    REMINDERS = 'Reminders', _('Reminders')
    POLITY = 'Polity', _('Polity')
    ECONOMY = 'Economy', _('Economy')
    GEOGRAPHY = 'Geography', _('Geography')
    HISTORY = 'History', _('History')
    SCIENCE_TECH = 'Science & Tech', _('Science & Tech')
    ENVIRONMENT = 'Environment', _('Environment')
    CURRENT_AFFAIRS = 'Current Affairs', _('Current Affairs')
    UNMARKED = 'Unmarked', _('Unmarked')

class Journal(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    long_term_goal = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    goal = models.ForeignKey(LongTermGoal, on_delete=models.CASCADE, related_name='journal_entries', null=True, blank=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    category = models.CharField(
        max_length=30,
        choices=JournalCategory.choices,
        default=JournalCategory.UNMARKED
    )
    
    PRIORITY_CHOICES = [
        ('high', 'Urgent and Important'),
        ('medium', 'Not Urgent but Important'),
        ('low', 'Urgent but Not Important'),
        ('lowest', 'Not Urgent and Not Important')
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')

    def is_protected(self):
        return bool(self.password)

    def save(self, *args, **kwargs):
        # Hash the password before saving if it exists
        if self.password:
            self.password = make_password(self.password)

        # Optionally, validate category (though already handled by `choices`)
        if self.category not in [choice[0] for choice in JournalCategory.choices]:
            raise ValueError(f"Invalid category: {self.category}")
        
        # Call the parent class's save method
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class DailyQuote(models.Model):
    quote = models.TextField()
    date = models.DateField(default=now, unique=True)
    is_homepage = models.BooleanField(default=False)

    def __str__(self):
        return f"Quote for {self.date}: {self.quote[:100]}"  # Shows the first 100 characters of the quote
