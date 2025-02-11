from rest_framework import serializers
from .models import Bid, ProposalTemplate

class BidSerializer(serializers.ModelSerializer):
    """
    Serializer for Bid model.
    """
    class Meta:
        model = Bid
        fields = '__all__'  # Serialize all fields in the model


class ProposalTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for ProposalTemplate model.
    """
    class Meta:
        model = ProposalTemplate
        fields = '__all__'  # Serialize all fields in the model
