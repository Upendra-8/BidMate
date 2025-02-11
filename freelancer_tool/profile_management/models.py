from django.db import models

class UserProfile(models.Model):
    freelancer_id = models.CharField(max_length=255)    # Unique ID from Freelancer API
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    skills = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "user_profile"