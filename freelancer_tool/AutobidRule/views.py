from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import AutobidRule
from .serializers import AutobidRuleSerializer
from .tasks import autobid_task  # Import your autobid_task function
from freelancer_tool.bidding.models import Bid
from freelancer_tool.bidding.serializers import BidSerializer
from django.db.models import Count, Q

class AutobidRuleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AutobidRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"success": "Rules saved successfully.", "rules": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        rules = AutobidRule.objects.filter(user=request.user).first()
        if not rules:
            return Response({"message": "No autobid rules found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AutobidRuleSerializer(rules)
        return Response({"rules": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request):
        rules = AutobidRule.objects.filter(user=request.user).first()
        if not rules:
            return Response({"error": "No rules to update. Please create rules first."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AutobidRuleSerializer(rules, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Rules updated successfully.", "rules": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post_autobid(self, request):
        """
        Trigger the autobid task for the logged-in user.
        """
        user = request.user
        result = autobid_task(user)  # Call the autobid task function
        return Response({"message": result}, status=status.HTTP_200_OK)

class BiddingHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_filter = request.query_params.get('status', None)
        bids = Bid.objects.filter(user=request.user)
        if status_filter:
            bids = bids.filter(status=status_filter)
        
        serializer = BidSerializer(bids, many=True)
        return Response({"status": "success", "data": serializer.data})

class BiddingAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_bids = Bid.objects.filter(user=request.user).count()
        successful_bids = Bid.objects.filter(user=request.user, status='won').count()
        success_rate = (successful_bids / total_bids) * 100 if total_bids > 0 else 0
        common_project_types = Bid.objects.values('proposal').annotate(count=Count('proposal')).order_by('-count')[:3]

        return Response({
            "status": "success",
            "data": {
                "total_bids": total_bids,
                "successful_bids": successful_bids,
                "success_rate": success_rate,
                "common_project_types": common_project_types
            }
        })
