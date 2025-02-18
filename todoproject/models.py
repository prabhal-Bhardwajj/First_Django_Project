'''
TODOPROJECT/MODELS.PY
'''
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
class DailyQuote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quote = models.TextField()
    date = models.DateField(default=now, unique=True)  # Ensure one quote per day

    def __str__(self):
        return f"Quote for {self.date}: {self.quote[:50]}"  # Show first 50 characters
