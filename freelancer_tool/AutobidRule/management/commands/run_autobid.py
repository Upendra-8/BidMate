from django.core.management.base import BaseCommand
from freelancer_tool.AutobidRule.tasks import autobid_task
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Run autobid tasks for users"

    def handle(self, *args, **kwargs):
        users = User.objects.all()  # You can filter this if needed
        for user in users:
            self.stdout.write(f"Running autobid for {user.username}")
            result = autobid_task(user)
            self.stdout.write(result)
