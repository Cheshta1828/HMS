from django.core.management.base import BaseCommand


from django.contrib.auth.models import Group
from accounts.models import Department
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission




class Command(BaseCommand):
    

    def handle(self, *args, **options):
        Doctors, created = Group.objects.get_or_create(name='Doctors')
        Doctors.save()
        Patients, created = Group.objects.get_or_create(name='Patients')
        Patients.save()
        

        # Create the admin user
       

        # Create customer1 user
        

        departments = [
            {
                'name': 'clinical',
                'diagnostics': 'Clinical diagnostics',
                'location': 'Location for Clinical',
                'specialization': 'Specialization for Clinical',
            },
            {
                'name': 'Teeth',
                'diagnostics': 'Teeth diagnostics',
                'location': 'Location for Teeth',
                'specialization': 'Specialization for Teeth',
            },
            # Add more departments here...
        ]

        for department_data in departments:
            department, created = Department.objects.get_or_create(**department_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Department "{department.name}" created successfully.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Department "{department.name}" already exists.'))

        self.stdout.write(self.style.SUCCESS('Groups and Departments created successfully.'))
        
