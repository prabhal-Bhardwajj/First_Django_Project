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
    GRATITUDE = 'Gratitude', _('Gratitude')
    INSIGHT = 'Insight', _('Insight')
    REFLECTION = 'Reflection', _('Reflection')
    MINDBYTE = 'Mindbyte', _('Mindbyte')
    MATHEMATICS = 'Mathematics', _('Mathematics')
    ASTROLOGY = 'Astrology', _('Astrology')
    MACHINE_LEARNING = 'Machine_Learning', _('Machine_Learning')
    PROGRAMMING = 'Programming', _('Programming')
    LITERATURE = 'Literature', _('Literature')
    POETRY = 'Poetry', _('Poetry')
    CINEMA = 'Cinema', _('Cinema')
    PHILOSOPHY = 'Philosophy', _('Philosophy')
    RELIGION = 'Religion', _('Religion')
    INFORMATION = 'Information', _('Information')
    THOUGHTS = 'Thoughts', _('Thoughts')
    TASKS = 'Tasks', _('Tasks')
    NOTES = 'Notes', _('Notes')
    NEWS = 'News', _('News')
    RANDOM = 'Random', _('Random')
    PHYSICS = 'Physics', _('Physics')
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
    DJANGO = 'Django', _('Django')
    ECONOMY = 'Economy', _('Economy')
    CULTURE = 'Culture', _('Culture')
    FRONT_END_PROGRAMMING = 'F_E_Programming', _('F_E_Programming')
    CPPLANGUAGE = 'CPP Language', _('CPP Language')
    GEOGRAPHY = 'Geography', _('Geography')
    JAVA = 'Java', _('Java')
    PYTHON = 'Python', _('Python')
    HISTORY = 'History', _('History')
    ART = 'Art', _('Art')
    MUSIC = 'Music', _('Music')
    SCIENCE_TECH = 'Science & Tech', _('Science & Tech')
    ASTRONOMY = 'Astronomy', _('Astronomy')
    BIOLOGY = 'Biology', _('Biology')
    STATISTICS = 'Statistics', _('Statistics')
    ENVIRONMENT = 'Environment', _('Environment')
    CURRENT_AFFAIRS = 'Current Affairs', _('Current Affairs')
    UNMARKED = 'Unmarked', _('Unmarked')

class Mood(models.TextChoices):
    HAPPY = 'Happy', _('Happy')
    FURIOUS = 'Furious', _('Furious')
    CONFUSED = 'Confused', _('Confused')
    BORED = 'Bored', _('Bored')
    REGRET = 'Regret', _('Regret')
    CALM = 'Calm', _('Calm')
    DEPRESSED = 'Depressed', _('Depressed')
    DISGUSTED = 'Disgusted', _('Disgusted')
    EUPHORIC = 'Euphoric', _('Euphoric')
    FRUSTRATED = 'Frustrated', _('Frustrated')
    GUILTY = 'Guilty', _('Guilty')
    HOPEFUL = 'Hopeful', _('Hopeful')
    HURT = 'Hurt', _('Hurt')
    INSECURE = 'Insecure', _('Insecure')
    JEALOUS = 'Jealous', _('Jealous')
    LONELY = 'Lonely', _('Lonely')
    LOVING = 'Loving', _('Loving')
    NERVOUS = 'Nervous', _('Nervous')
    OVERWHELMED = 'Overwhelmed', _('Overwhelmed')
    PROUD = 'Proud', _('Proud')
    SCARED = 'Scared', _('Scared')
    SHOCKED = 'Shocked', _('Shocked')
    SURPRISED = 'Surprised', _('Surprised')
    SAD = 'Sad', _('Sad')
    REVENGEFUL = 'Revengeful', _('Revengeful')
    SORRY = 'Sorry', _('Sorry')
    WORRIED = 'Worried', _('Worried')
    ANGRY = 'Angry', _('Angry')
    ANXIOUS = 'Anxious', _('Anxious')
    EXCITED = 'Excited', _('Excited')
    RELAXED = 'Relaxed', _('Relaxed')
    TIRED = 'Tired', _('Tired')
    ROMANTIC = 'Romantic', _('Romantic')
    CARELESS = 'Careless', _('Careless')
    EROTIC = 'Erotic', _('Erotic')
    GRATEFUL = 'Grateful', _('Grateful')
    INSPIRED = 'Inspired', _('Inspired')
    MOTIVATED = 'Motivated', _('Motivated')
    PEACEFUL = 'Peaceful', _('Peaceful')
    CONFIDENT = 'Confident', _('Confident')
    ASHAMED = 'Ashamed', _('Ashamed')
    EMBARRASSED = 'Embarrassed', _('Embarrassed')
    RESENTFUL = 'Resentful', _('Resentful')
    INDIFFERENT = 'Indifferent', _('Indifferent')
    HOPELESS = 'Hopeless', _('Hopeless')
    DISAPPOINTED = 'Disappointed', _('Disappointed')
    DISAPPROVING = 'Disapproving', _('Disapproving')
    DISBELIEVING = 'Disbelieving', _('Disbelieving')
    DISCOURAGED = 'Discouraged', _('Discouraged')
    DISCONNECTED = 'Disconnected', _('Disconnected')
    STRESSED = 'Stressed', _('Stressed')
    NEUTRAL = 'Neutral', _('Neutral')
    UNMARKED = 'Unmarked', _('Unmarked')
    
    

    def __str__(self):
        return self.name
class Journal(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    long_term_goal = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    goal = models.ForeignKey(LongTermGoal, on_delete=models.CASCADE, related_name='journal_entries', null=True, blank=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    mood = models.CharField(
        max_length=20,
        choices=Mood.choices,
        default=Mood.UNMARKED
    )
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

