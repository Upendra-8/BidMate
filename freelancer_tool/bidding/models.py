from django.db import models
from django.contrib.auth.models import User

class Bid(models.Model):
    project_id = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    proposal = models.TextField()
    period = models.IntegerField()
    milestone_percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid on Project {self.project_id} by {self.bidder.username}"


class ProposalTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return f"Template: {self.title} by {self.user.username}"

