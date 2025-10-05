from django.db import models
from django.utils import timezone

class Feedback(models.Model):
    token = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)
    line = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    geo_location = models.CharField(max_length=100)  # Could be changed to a more appropriate field type

    def __str__(self):
        return f"Feedback {self.id} for line {self.line} to {self.destination}"

class EmailVerification(models.Model):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def is_recent(self):
        return timezone.now() - self.created_at <= timezone.timedelta(hours=1)

    def __str__(self):
        return f"EmailVerification(email={self.email}, verified={self.verified})"