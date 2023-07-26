from rest_framework.permissions import BasePermission
from .models import customuser,PatientRecord,Department

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user has the "Doctors" group
        if request.user.groups.filter(name='Doctors').exists():
            # Check if the user's role is 1 (doctor)
            return request.user.role == customuser.DOCTOR

        return False

class IsRelevantPatientOrDoctor(BasePermission):
    def has_permission(self, request, view):
        patient_id = view.kwargs.get('pk')
        patient_record = PatientRecord.objects.filter(pk=patient_id).first()

        if not patient_record:
            return False

        if request.user.role == customuser.PATIENT:
            # Only the relevant patient can access their own record
            return request.user == patient_record.patient_id

        if request.user.role == customuser.DOCTOR:
            # Only the relevant doctor from the same department can access the patient record
            return request.user.department == patient_record.department.name

        return False
class IsDoctorInDepartment(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is a doctor and belongs to the same department as the patient's record
        if request.user.role == customuser.DOCTOR and request.user.department == obj.patient_id.department:
            return True
        return False
    
class IsPatientOrRelevantDoctor(BasePermission):
    def has_permission(self, request, view):
        
        patient_id = view.kwargs['pk']
        return request.user.role == customuser.PATIENT or (request.user.role == customuser.DOCTOR and PatientRecord.objects.filter(patient_id=patient_id,
department__name=request.user.department).exists())