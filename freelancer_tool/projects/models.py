from django.db import models

class Project(models.Model):
    """
    Model to store project details.
    """
    project_id = models.CharField(max_length=255, unique=True)  # Store the Freelancer project ID
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2)
    skills = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    bids_placed = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "project"

