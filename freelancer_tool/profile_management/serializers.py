from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['freelancer_id', 'name', 'country', 'skills', 'updated_at']  # Include necessary fields only
