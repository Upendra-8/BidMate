from rest_framework import serializers
from freelancer_tool.bidding.models import Bid  # Importing Bid from Sprint 3

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'project_id', 'bidder', 'amount', 'proposal', 'period', 'milestone_percentage', 'created_at']

# Delay the import of AutobidRule to avoid circular import
class AutobidRuleSerializer(serializers.ModelSerializer):
    bids = BidSerializer(many=True, read_only=True)  # Include associated bids in the serialized data

    class Meta:
        # Dynamically import the model using Django's apps.get_model() to avoid circular import
        from django.apps import apps
        AutobidRule = apps.get_model('freelancer_tool', 'AutobidRule')
        model = AutobidRule
        fields = ['id', 'user', 'exclude_countries', 'include_skills', 'payment_verified_only', 'min_budget', 'max_budget', 'enabled', 'bids']
