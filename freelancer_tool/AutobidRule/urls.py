from django.urls import path
from .views import AutobidRuleView, BiddingHistoryView, BiddingAnalyticsView

urlpatterns = [
    path('autobid/rules/', AutobidRuleView.as_view(), name='autobid_rules'),
    path('history/', BiddingHistoryView.as_view(), name='bidding_history'),
    path('history/stats/', BiddingAnalyticsView.as_view(), name='bidding_analytics'),
]
