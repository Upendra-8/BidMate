# Freelancer Automation Tool
## Overview
The Freelancer Automation Tool is a Python-based project designed to automate bidding on Freelancer.com projects. It enables users to search, filter, and place bids on projects using predefined rules and templates. The tool provides both manual and automated bidding functionalities.
## Features
- ## Authentication & Profile Management
  - Secure login using Freelancer API
  - Logout to revoke access token
  - Fetch and sync profile details (name, country, skills)
- ## Project Search & Listing
  - Search for projects based on user skills
  - Filter projects by Country, Project type (hourly/fixed)
  - View detailed project information
- ## Manual Bid Placement
  - Place a bid with a custom proposal and price
  - Save reusable proposal templates
  - View all placed bids with their status
- ## Auto Bidding
  - Define autobidding rules (e.g., exclude specific countries, use templates)
  - Set a timer for automated bids
  - Start and stop the autobidding service
  - Monitor autobidding activity

## Installation
## Prerequisites
Ensure you have the following installed:

- Python 3.8+

- Django 5.x or higher

- Django REST Framework (DRF)

## Setup
1. Clone the Repository
git clone https://github.com/yourusername/BidMate.git

2. Create and Activate a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

## Running the Application
1. Start the Development Server
python manage.py runserver
2. Access the Application
Navigate to http://127.0.0.1:8000/ in your web browser or use tools like Postman for API testing.

## Usage
You can use either Postman or Thunder Client to interact with the API.
    
## Contributing

We welcome contributions to improve the project. To contribute:

1. Fork the repository.

2. Create a new branch (git checkout -b feature-branch).

3. Make your changes.

4. Commit your changes (git commit -am 'Add new feature').

5. Push your branch (git push origin feature-branch).

6. Open a Pull Request.
   
## Acknowledgments
- **Django REST Framework:** Used for building the API endpoints.
