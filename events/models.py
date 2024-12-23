from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    EVENT_MODES = [
        ('in-person', 'In-Person'),
        ('online', 'Online'),
        ('zoom', 'Zoom'),
        ('google-meet', 'Google Meet'),
        ('webex', 'Webex'),
    ]

    EVENT_CATEGORIES = [
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('meetup', 'Meetup'),
    ]

    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EVENT_CATEGORIES)
    is_urgent = models.BooleanField(default=False)
    is_approaching = models.BooleanField(default=False)
    mode = models.CharField(max_length=20, choices=EVENT_MODES)
    location = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

