from django.db import models
from django.utils import timezone

class Todo(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField(blank=True, null=True)
    context = models.CharField(max_length=200, blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    due_date = models.DateField(default='2025-1-1')
    completed = models.BooleanField(default=False)
    is_long_term_goal = models.BooleanField(default=False)
    
    
    PRIORITY_CHOICES = [
        ('high', 'Urgent and Important'),
        ('medium', 'Not Urgent but Important'),
        ('low', 'Urgent but Not Important'),
        ('lowest', 'Not Urgent and Not Important')
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Save the Todo object
        super().save(*args, **kwargs)
        # Update TaskCounter whenever a task is added or updated
        self.update_task_counter()

    def update_task_counter(self):
        """Update the TaskCounter for the day whenever a task is completed or added."""
        task_counter, created = TaskCounter.objects.get_or_create(date=self.due_date)
        task_counter.update_counts()


class LongTermGoal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    

    PRIORITY_CHOICES = [
        ('high', 'Urgent and Important'),
        ('medium', 'Not Urgent but Important'),
        ('low', 'Urgent but Not Important'),
        ('lowest', 'Not Urgent and Not Important')
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Save the LongTermGoal object
        super().save(*args, **kwargs)
        # Update TaskCounter whenever a long-term goal is added or updated
        self.update_task_counter()

    def update_task_counter(self):
        """Update the TaskCounter for the day whenever a long-term goal is completed or added."""
        task_counter, created = TaskCounter.objects.get_or_create(date=self.due_date)
        task_counter.update_counts()


class TaskCounter(models.Model):
    date = models.DateField(default=timezone.now)
    today_completed = models.IntegerField(default=0)
    today_incomplete = models.IntegerField(default=0)
    longgoal_complete = models.IntegerField(default=0)
    longgoal_incomplete = models.IntegerField(default=0)

    def update_counts(self):
        """Update the counts of completed and incomplete tasks and goals for the day."""
        today_todo = Todo.objects.filter(due_date=self.date)
        self.today_completed = today_todo.filter(completed=True).count()
        self.today_incomplete = today_todo.filter(completed=False).count()

        today_goals = LongTermGoal.objects.filter(due_date=self.date)
        self.longgoal_complete = today_goals.filter(completed=True).count()
        self.longgoal_incomplete = today_goals.filter(completed=False).count()

        self.save()

    def get_total_completed(self):
        """Get total completed tasks and goals for the day."""
        return self.today_completed + self.longgoal_complete

    def get_total_incomplete(self):
        """Get total incomplete tasks and goals for the day."""
        return self.today_incomplete + self.longgoal_incomplete

    def __str__(self):
        return (f"DATE: {self.date} - "
                f"Todos: Completed: {self.today_completed}, Incomplete: {self.today_incomplete}; "
                f"Goals: Completed: {self.longgoal_complete}, Incomplete: {self.longgoal_incomplete}")
