from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Intention(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    created_datetime = models.DateTimeField(default=timezone.now)

    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    completed = models.BooleanField(default=False)
    neverminded = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_datetime']

    def __str__(self):
        return self.title

    def get_status(self):
        if self.completed:
            return 'completed'
        elif self.neverminded:
            return 'neverminded'
        else:
            return 'active'
