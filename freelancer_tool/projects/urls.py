from django.urls import path
from .views import search_projects, project_details #list_active_projects #add_skill, place_bid

urlpatterns = [
    path('search/', search_projects, name='project_search'),
    path('details/<int:project_id>/', project_details, name='project_detail'),  # View project details by project_id
    
]

