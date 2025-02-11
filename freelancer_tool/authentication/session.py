import requests
from freelancersdk.session import Session
from freelancersdk.exceptions import AuthTokenNotSuppliedException
from django.conf import settings

class FreelancerOAuthSession:
    def __init__(self, oauth_token=None, sandbox_mode=True):
        """
        Initializes the FreelancerOAuthSession with the given OAuth token.
        """
        base_url = "https://www.freelancer.com/api"
        if sandbox_mode:
            base_url = "https://www.freelancer-sandbox.com/api"

        if not oauth_token:
            raise AuthTokenNotSuppliedException("OAuth token not supplied")

        # Initialize the session with the provided OAuth token and base URL
        self.session = Session(oauth_token=oauth_token, url=base_url)

    @staticmethod
    def get_authorize_url():
        """
        Generates the Freelancer OAuth URL to redirect users to for authentication.
        """
        config = settings.FREELANCER_OAUTH
        redirect_uri_encoded = config['REDIRECT_URI']  # Ensure URL is correctly encoded
        return (
            f"{config['AUTHORIZE_URL']}?response_type=code"
            f"&client_id={config['CLIENT_ID']}"
            f"&redirect_uri={redirect_uri_encoded}"
            f"&scope=basic%20profile%20jobs%20portfolio"
            f"&prompt=select_account%20consent"
        )

    @staticmethod
    def get_access_token(auth_code):
        """
        Exchanges the authorization code for an access token.
        """
        config = settings.FREELANCER_OAUTH
        payload = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'client_id': config['CLIENT_ID'],
            'client_secret': config['CLIENT_SECRET'],
            'redirect_uri': config['REDIRECT_URI'],
        }
        try:
            # Request the access token from Freelancer API
            response = requests.post(config['TOKEN_URL'], data=payload)
            response.raise_for_status()  # Raise exception for invalid responses
            return response.json()  # Return the response JSON with token data
        except requests.RequestException as e:
            print("Error response:", response.text)  # Print full error response for debugging
            raise e  # Reraise the exception after logging it

    def logout(self):
        """
        Logs out the user by closing the session.
        """
        self.session.session.close()  # Close the session to log out
        return "Logged out successfully"

    def get_user_profile(self):
        try:
            # Make the API call to fetch the user's profile
            url = f"{self.session.url}/users/0.1/self/"
            response = self.session.session.get(url)
            response.raise_for_status()

            # Log the raw response for debugging
            api_response = response.json()
            print("API Response:", api_response)  # Log the entire response

            user_data = api_response.get('result', None)

            if not user_data:
                print("No user data found in API response.")
                return None

            # Debugging: Print out the structure to confirm where skills and email are located
            print("User   data structure:", user_data)

            # Extract email
            email = user_data.get("email")
            if email is None:
                print("Email not found in user data.")

            # Extract skills
            skills_data = user_data.get("skills", [])
            if not skills_data:
                print("No skills found in profile.")

            # Ensure skills are properly formatted
            skills = [skill["name"] for skill in skills_data] if skills_data else ["No skills listed"]

            # Extract payment verification status
            payment_verified = user_data.get("status", {}).get("payment_verified", False)

            # Return the processed user profile data
            return {
                "id": user_data.get("id"),
                "username": user_data.get("username"),
                "email": email if email else "Email not available",
                "skills": skills,  # List of skills
                "country": user_data.get("location", {}).get("country", {}).get("name", "Not available"),
                "payment_verified": payment_verified,
            }

        except requests.RequestException as e:
            print(f"Error fetching user profile: {e}")
            return None