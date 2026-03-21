from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    completed = models.BooleanField(default=False)

    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title