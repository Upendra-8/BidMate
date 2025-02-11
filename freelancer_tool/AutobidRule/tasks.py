import requests
from .models import AutobidRule
from freelancer_tool.bidding.models import Bid, ProposalTemplate

def autobid_task(user):
    rules = AutobidRule.objects.filter(user=user, enabled=True).first()
    if not rules:
        return "No active autobid rules."

    access_token = user.auth_token.key  # Assuming Token Authentication
    headers = {"Authorization": f"Bearer {access_token}"}

    # Fetch projects
    response = requests.get(
        "https://www.freelancer-sandbox.com/api/projects/0.1/projects/active/",
        headers=headers,
    )
    if response.status_code != 200:
        return "Failed to fetch projects."

    projects = response.json().get('result', {}).get('projects', [])
    matched_projects = []

    for project in projects:
        # Apply rules
        if any(skill['name'] in rules.include_skills for skill in project.get('jobs', [])):
            if project['budget']['minimum'] >= rules.min_budget and project['budget']['maximum'] <= rules.max_budget:
                if project['currency']['country'] not in rules.exclude_countries:
                    if rules.payment_verified_only and not project.get('payment_verified', False):
                        continue
                    matched_projects.append(project)

    # Place bids
    for project in matched_projects:
        bid_response = requests.post(
            "https://www.freelancer-sandbox.com/api/projects/0.1/bids/",
            headers=headers,
            json={
                "project_id": project['id'],
                "amount": project['budget']['minimum'],
                "period": 7,
                "proposal": ProposalTemplate.objects.filter(user=user).first().content,
                "milestone_percentage": 50,
            },
        )
        if bid_response.status_code == 201:
            Bid.objects.create(
                project_id=project['id'],
                bidder=user,
                amount=project['budget']['minimum'],
                proposal=ProposalTemplate.objects.filter(user=user).first().content,
                period=7,
                milestone_percentage=50,
            )
    return f"{len(matched_projects)} bids placed."
