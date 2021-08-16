from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

def get_working_day_date():
    datetime = timezone.now()
    next_day_starts_at = 4
    if datetime.hour < next_day_starts_at:
        return datetime.date() - timezone.timedelta(days=1)
    else:
        return datetime.date()

class Intention(models.Model):
    title = models.CharField(max_length=500)
    date = models.DateField(default=get_working_day_date)
    created_datetime = models.DateTimeField(default=timezone.now)

    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    completed = models.BooleanField(default=False)
    neverminded = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_datetime']

    def __str__(self):
        return self.title

    def get_status(self):
        if self.completed:
            return 'completed'
        elif self.neverminded:
            return 'neverminded'
        else:
            return 'active'

class IntentionsDraft(models.Model):
    content = models.TextField()
    date = models.DateField(default=get_working_day_date)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_datetime = models.DateTimeField(default=timezone.now)
    version = models.IntegerField(default=0)  # Needed for autosaving

    class Meta:
        constraints = [models.UniqueConstraint(fields=['date', 'creator'], name='One intentions draft per user per day')]

class Note(models.Model):
    content = models.TextField()
    date = models.DateField(default=get_working_day_date)
    created_datetime = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    version = models.IntegerField(default=0)  # Needed for autosaving

    class Meta:
        constraints =[models.UniqueConstraint(fields=['date','creator'],name='One note per user per day')]

        ordering = ['-created_datetime']
