from django.db import models
from django.contrib.auth.models import User
from freelancer_tool.bidding.models import Bid  # Importing Bid from Sprint 3

class AutobidRule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exclude_countries = models.TextField(blank=True)  # Comma-separated country names
    include_skills = models.TextField(blank=True)    # Comma-separated skills
    payment_verified_only = models.BooleanField(default=True)
    min_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    enabled = models.BooleanField(default=False)
    bids = models.ManyToManyField(Bid, blank=True, related_name="autobid_rules")  # Track associated bids

    def __str__(self):
        return f"Autobid Rules for {self.user.username}"
