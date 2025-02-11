from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Bid, ProposalTemplate
from .serializers import BidSerializer, ProposalTemplateSerializer
import requests


class PlaceBidView(APIView):
    """
    Place a custom bid on a project using Freelancer Sandbox APIs.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Debugging: Log the request headers
        print("Request Headers:", request.headers)

        # Extract the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)

        access_token = auth_header.split('Bearer ')[-1]

        # Extract data from the request body
        try:
            project_id = request.data.get("project_id")
            bid_amount = request.data.get("amount")
            bid_period = request.data.get("period")
            bidder_id = request.data.get("owner_id")
            milestone_percentage = request.data.get("milestone_percentage", 50)

            # Validate required fields
            if not all([project_id, bid_amount, bid_period, bidder_id]):
                return Response({'error': 'Missing required fields: project_id, amount, period, or owner_id.'}, status=status.HTTP_400_BAD_REQUEST)

            # Call Freelancer API to place a bid
            payload = {
                "project_id": project_id,
                "amount": bid_amount,
                "period": bid_period,
                "owner_id": bidder_id,
                "milestone_percentage": milestone_percentage
            }
            bid_response = requests.post(
                "https://www.freelancer-sandbox.com/api/projects/0.1/bids/",
                headers={"Authorization": f"Bearer {access_token}"},
                json=payload
            )

            if bid_response.status_code != 201:
                return Response(
                    {'error': 'Failed to place bid', 'details': bid_response.json()},
                    status=bid_response.status_code
                )

            # Save bid locally in the database
            user = request.user
            bid = Bid.objects.create(
                project_id=project_id,
                bidder=user,
                amount=bid_amount,
                proposal=f"Bid on project {project_id}",
                period=bid_period,
                milestone_percentage=milestone_percentage
            )

            return Response({"success": "Bid placed successfully.", "data": BidSerializer(bid).data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SaveTemplateView(APIView):
    """
    Save proposal templates for quick reuse.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Validate template data using ProposalTemplateSerializer
        serializer = ProposalTemplateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save template with the current user
        validated_data = serializer.validated_data
        user = request.user  # Use the authenticated user
        template = ProposalTemplate.objects.create(
            user=user,
            title=validated_data['title'],
            content=validated_data['content']
        )
        return Response(
            {"success": "Template saved successfully.", "template": ProposalTemplateSerializer(template).data},
            status=status.HTTP_201_CREATED
        )


class ListTemplatesView(APIView):
    """
    List all saved proposal templates for a user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve templates for the current user
        templates = ProposalTemplate.objects.filter(user=request.user)
        if not templates.exists():
            return Response({"message": "No templates found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and return the templates
        serializer = ProposalTemplateSerializer(templates, many=True)
        return Response(
            {"success": "Templates retrieved successfully.", "templates": serializer.data},
            status=status.HTTP_200_OK
        )
