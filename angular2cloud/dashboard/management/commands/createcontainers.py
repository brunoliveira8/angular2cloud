from django.core.management.base import BaseCommand, CommandError
from dashboard.models import Project
from dashboard.utils import run_container

class Command(BaseCommand):
    help = 'Create and run all project containers'

    def handle(self, *args, **options):
        for project in Project.objects.all():
            run_container(project)
