from django.urls import path
from .views import PlaceBidView, SaveTemplateView, ListTemplatesView

urlpatterns = [
    path('bids/', PlaceBidView.as_view(), name='place_bid'),
    path('templates/', SaveTemplateView.as_view(), name='save_template'),
    path('templates/list/', ListTemplatesView.as_view(), name='list_templates'),
]
