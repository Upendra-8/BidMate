from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import requests
from .models import UserProfile
from .serializers import UserProfileSerializer
from freelancer_tool.authentication.session import FreelancerOAuthSession
from rest_framework.permissions import AllowAny


class SyncProfileView(APIView):
    permission_classes = [AllowAny]
    """
    Fetches and stores Freelancer profile details locally. This now uses POST instead of GET.
    """

    def post(self, request):
        access_token = request.data.get('access_token')  # Assuming the access token is sent in the request body
        if not access_token:
            return Response({"error": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        try:
            # Call Freelancer API to fetch user profile
            url = 'https://www.freelancer-sandbox.com/api/users/0.1/self/'
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                return Response({"error": "Failed to sync profile", "details": response.text}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            user_data = response.json().get("result", None)

            if not user_data:
                return Response({"error": "User data not found"}, status=status.HTTP_404_NOT_FOUND)

            # Debugging: print the entire response
            print("Full API Response:", response.json())  # This will help us examine the structure of the response

            # Safely handle the qualifications key
            qualifications = user_data.get("qualifications", [])
            if qualifications is None:
                qualifications = []  # Default to an empty list if None

            # Extract skills from qualifications
            skills = ", ".join([q.get("name") for q in qualifications if q.get("name")])

            # Create or update the user profile
            user_profile, _ = UserProfile.objects.update_or_create(
                freelancer_id=user_data["id"],
                defaults={
                    "freelancer_id": user_data["id"],
                    "name": user_data.get("display_name", "N/A"),
                    "country": user_data.get("location", {}).get("country", {}).get("name", "Unknown"),
                    "skills": skills if skills else "None",
                }
            )

            # Serialize the updated user profile
            serialized_data = UserProfileSerializer(user_profile).data
            return Response({"message": "Profile synced successfully", "profile": serialized_data}, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            return Response({"error": "Failed to sync profile", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ViewProfileView(APIView):
    permission_classes = [AllowAny]
    """
    Displays the locally stored profile details.
    """
    def get(self, request):
        # Retrieve the first user profile
        user_profile = UserProfile.objects.first()  # Assuming single-user setup
        if not user_profile:
            return Response({"error": "Profile not found. Please sync first."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the profile
        serialized_data = UserProfileSerializer(user_profile).data
        return Response({"profile": serialized_data}, status=status.HTTP_200_OK)
