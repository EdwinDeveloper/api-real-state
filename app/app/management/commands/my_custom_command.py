from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Executes the custom command'

    def handle(self, *args, **options):
        # Add your custom command logic here
        print("Running my custom command every 5 seconds...")
