from django.urls import path
from .views import SyncProfileView, ViewProfileView

urlpatterns = [
    path('sync/', SyncProfileView.as_view(), name='sync_profile'),
    path('view/', ViewProfileView.as_view(), name='view_profile'),
]
