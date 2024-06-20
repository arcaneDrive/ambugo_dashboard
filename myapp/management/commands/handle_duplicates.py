# myapp/management/commands/handle_duplicates.py

from django.core.management.base import BaseCommand
from myapp.models import Ambulance
from django.db.models import Count

class Command(BaseCommand):
    help = 'Handle duplicates in Ambulance model'

    def handle(self, *args, **options):
        # Find duplicate driver names
        duplicates = Ambulance.objects.values('driver_name').annotate(count=Count('driver_name')).filter(count__gt=1)

        for duplicate in duplicates:
            driver_name = duplicate['driver_name']
            duplicate_entries = Ambulance.objects.filter(driver_name=driver_name)

            # Modify the duplicates by appending a unique identifier
            for index, entry in enumerate(duplicate_entries):
                entry.driver_name = f"{driver_name}_{index}"  # Modify the driver_name
                entry.save()  # Save the modified entry

        self.stdout.write(self.style.SUCCESS('Duplicates handled successfully.'))
