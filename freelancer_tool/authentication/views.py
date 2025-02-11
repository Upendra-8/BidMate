import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.http import JsonResponse
from .session import FreelancerOAuthSession
from rest_framework.permissions import AllowAny


class RedirectToOAuthView(APIView):
    """
    Redirects the user to the Freelancer OAuth authorization URL.
    """
    permission_classes = [AllowAny]  # Allow access without authentication

    def get(self, request):
        try:
            # Get the Freelancer OAuth authorization URL
            auth_url = FreelancerOAuthSession.get_authorize_url()
            return redirect(auth_url)  # Redirect the user to the authorization URL
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class FreelancerOAuthCallbackView(APIView):
    """
    Handles the OAuth callback and receives the authorization code.
    """
    permission_classes = [AllowAny]  # Allow any user to access this view

    def get(self, request):
        auth_code = request.GET.get('code')  # Extract the authorization code from the query string
        if not auth_code:
            return JsonResponse({"error": "Authorization code is required"}, status=400)

        # Store the auth code in session (optional)
        request.session['auth_code'] = auth_code

        return JsonResponse({
            "message": "Authorization code received",
            "auth_code": auth_code
        })


class LoginView(APIView):
    """
    Handles login with the Freelancer OAuth token.
    Exchanges the authorization code for an access token.
    """
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        auth_code = request.data.get('auth_code')  # Authorization code sent from the client

        if not auth_code:
            return Response({"error": "Authorization code is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Exchange the authorization code for an access token
            token_data = FreelancerOAuthSession.get_access_token(auth_code)
            access_token = token_data['access_token']

            # Store access token in session
            request.session['access_token'] = access_token

            return Response({
                "message": "Login successful",
                "access_token": access_token
            })
        except requests.RequestException as e:
            return Response({
                "error": "Failed to authenticate",
                "details": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Handles logout by invalidating the session and access token.
    """
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request):
        # Get the access token from the Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        access_token = None

        if auth_header and auth_header.startswith('Bearer '):
            access_token = auth_header.split(' ')[1]  # Extract the token

        # Debugging: Log the access token
        print(f"Access Token: {access_token}")  # This will print to the console

        if access_token:
            # Initialize the session with the provided access token and log out
            oauth_session = FreelancerOAuthSession(oauth_token=access_token)
            try:
                oauth_session.logout()  # Close the session (if supported by the API)
            except Exception as e:
                return Response({"error": "Failed to log out from the OAuth provider", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            # Clear session data in Django
            request.session.flush()  # This will remove all session data
            return Response({"message": "Logout successful"})

        return Response({"error": "No active session"}, status=status.HTTP_400_BAD_REQUEST)




class AuthStatusView(APIView):
    """
    Checks if the user is authenticated and fetches their profile data.
    """
    permission_classes = [AllowAny]
    def get(self, request):
        access_token = request.session.get('access_token')
        if not access_token:
            return Response({"message": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            oauth_session = FreelancerOAuthSession(oauth_token=access_token)
            user_profile = oauth_session.get_user_profile()

            if not user_profile:
                return Response({"message": "Failed to fetch user profile"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "status": "authenticated",
                "user": user_profile
            })

        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
