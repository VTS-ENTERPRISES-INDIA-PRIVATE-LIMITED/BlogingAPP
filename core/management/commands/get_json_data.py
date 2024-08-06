from django.core.management.base import BaseCommand
from core.models import EmpID
import json
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Load employee IDs from a JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file')

    def handle(self, *args, **options):
        json_file_path = options['json_file']
        
        if not os.path.isfile(json_file_path):
            self.stderr.write(self.style.ERROR(f'File not found: {json_file_path}'))
            return

        try:
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
                emp_ids = data.get('valid_emp_ids', [])

                # Check if emp_ids is a list
                if not isinstance(emp_ids, list):
                    self.stderr.write(self.style.ERROR('Invalid data format in JSON file'))
                    return

                # Bulk create EmpID instances
                EmpID.objects.bulk_create([EmpID(emp_id=emp_id) for emp_id in emp_ids])

                self.stdout.write(self.style.SUCCESS('Successfully loaded employee IDs into the database'))

        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR('Error decoding JSON file'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))
