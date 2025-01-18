'''
MODELS OF JOURNAL
'''
from django.db import models
from todoapp.models import LongTermGoal
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now

class Journal(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    long_term_goal = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    goal = models.ForeignKey(LongTermGoal, on_delete=models.CASCADE, related_name='journal_entries', null=True, blank=True)
    password = models.CharField(max_length=128, blank=True, null=True)
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
        if self.password:
            self.password = make_password(self.password)  # Hash the password before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class DailyQuote(models.Model):
    quote = models.TextField()
    date = models.DateField(default=now, unique=True)
    is_homepage = models.BooleanField(default=False)

    def __str__(self):
        return f"Quote for {self.date}: {self.quote[:100]}"  # Shows the first 100 characters of the quote
