from django.http import JsonResponse
from freelancer_tool.authentication.session import FreelancerOAuthSession
import requests
from rest_framework.permissions import AllowAny

def get_access_token(request):
    permission_classes = [AllowAny]
    """
    Retrieve the access token either from the session or Authorization header.
    """
    # Check for token in session first
    access_token = request.session.get('access_token')
    if not access_token:
        # Check the Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            access_token = auth_header.split(' ')[1]
    return access_token


def validate_access_token(access_token):
    permission_classes = [AllowAny]
    """
    Validates the Freelancer OAuth access token using the `/users/0.1/self/` endpoint.
    """
    verification_url = "https://www.freelancer-sandbox.com/api/users/0.1/self/"
    headers = {"freelancer-oauth-v1": access_token}
    response = requests.get(verification_url, headers=headers)
    if response.status_code == 200:
        return True
    return False


def search_projects(request):
    permission_classes = [AllowAny]
    """
    Searches for Freelancer projects based on user's skills and preferences.
    """
    # Retrieve the access token
    access_token = get_access_token(request)
    if not access_token:
        return JsonResponse({"status": "error", "message": "User not authenticated. Please log in."}, status=401)

    # Validate the access token
    if not validate_access_token(access_token):
        return JsonResponse({"status": "error", "message": "Invalid or expired token. Please log in again."}, status=401)

    # Initialize the OAuth session
    oauth_session = FreelancerOAuthSession(oauth_token=access_token)
    url = f"{oauth_session.session.url}/projects/0.1/projects/active/"

    # API Query Parameters (empty because no manual parameters are passed)
    params = {}

    try:
        # Make the GET request to Freelancer API
        response = oauth_session.session.session.get(url, params=params)
        response.raise_for_status()
        return JsonResponse(response.json(), safe=False)  # Return the API's JSON response
    except requests.exceptions.HTTPError as http_err:
        return JsonResponse({"status": "error", "message": "Failed to fetch projects", "details": str(http_err)}, status=response.status_code)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "An unexpected error occurred", "details": str(e)}, status=500)


def project_details(request, project_id):
    permission_classes = [AllowAny]
    """
    Fetches details of a specific Freelancer project by project ID.
    """
    # Retrieve the access token
    access_token = get_access_token(request)
    if not access_token:
        return JsonResponse({"status": "error", "message": "User not authenticated. Please log in."}, status=401)

    # Validate the access token
    if not validate_access_token(access_token):
        return JsonResponse({"status": "error", "message": "Invalid or expired token. Please log in again."}, status=401)

    # Initialize the OAuth session
    oauth_session = FreelancerOAuthSession(oauth_token=access_token)
    url = f"{oauth_session.session.url}/projects/0.1/projects/{project_id}/"

    try:
        # Make the GET request to Freelancer API
        response = oauth_session.session.session.get(url)
        response.raise_for_status()
        return JsonResponse(response.json(), safe=False)  # Return the API's JSON response
    except requests.exceptions.HTTPError as http_err:
        return JsonResponse({"status": "error", "message": "Failed to fetch project details", "details": str(http_err)}, status=response.status_code)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "An unexpected error occurred", "details": str(e)}, status=500)
