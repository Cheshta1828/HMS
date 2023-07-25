from django.contrib.auth.models import AbstractUser
from django.db import models
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    diagnostics = models.TextField()
    location = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class customuser(AbstractUser):
    DOCTOR = 1
    PATIENT = 2

    
    ROLE_CHOICES = (
        (DOCTOR, 'Doctor'),
        (PATIENT, 'patient')
    )



    
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,default=PATIENT,blank=False)
    department = models.TextField()
    
class PatientRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(customuser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    diagnostics = models.TextField()
    observations = models.TextField()
    treatments = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    misc = models.TextField()

    def __str__(self):
        return f"Record ID: {self.record_id}, Patient ID: {self.patient_id}"
    