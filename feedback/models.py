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
    email = models.EmailField()
    token = models.CharField(max_length=64, unique=True)
    device_id = models.CharField(max_length=100, blank=True)
    platform = models.CharField(max_length=20, default='web')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['email']),
            models.Index(fields=['email', 'verified']),
        ]

    def __str__(self):
        status = "verified" if self.verified else "pending"
        return f"{self.email} ({self.platform}) - {status}"

class RideFeedback(models.Model):
    movement_id = models.CharField(max_length=100)
    line_name = models.CharField(max_length=100)
    direction = models.CharField(max_length=100)
    feedback_timestamp = models.DateTimeField()
    punctuality = models.CharField(max_length=50, blank=True, null=True)
    onboard_info_display = models.CharField(max_length=50, blank=True, null=True)
    onboard_announcements = models.CharField(max_length=50, blank=True, null=True)
    capacity = models.CharField(max_length=50, blank=True, null=True)
    driving_style = models.CharField(max_length=50, blank=True, null=True)
    cleanliness = models.JSONField(blank=True, null=True)  # Storing list of cleanliness issues
    temperature = models.CharField(max_length=50, blank=True, null=True)
    passenger_behavior = models.CharField(max_length=50, blank=True, null=True)
    additional_comments = models.TextField(blank=True, null=True)
    token = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RideFeedback {self.id} for movement {self.movement_id}"
