from rest_framework import serializers
from .models import Project #Bid, ProposalTemplate

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'budget_min', 'budget_max', 'skills', 'country', 'status', 'bids_placed']



