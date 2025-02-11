from django.urls import path
from .views import RedirectToOAuthView, FreelancerOAuthCallbackView, LoginView, LogoutView, AuthStatusView

urlpatterns = [
    path('auth/redirect/', RedirectToOAuthView.as_view(), name='auth_redirect'),
    path('verify-profile/', FreelancerOAuthCallbackView.as_view(), name='oauth_callback'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/status/', AuthStatusView.as_view(), name='auth_status'),
]
