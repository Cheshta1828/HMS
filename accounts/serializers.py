from rest_framework import serializers
from .models import customuser, PatientRecord, Department
from rest_framework.response import Response
from rest_framework import generics, status, permissions
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DepartmentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('name',)

class PatientRecordSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    department = DepartmentNameSerializer('department')  # Use the new DepartmentNameSerializer

    class Meta:
        model = PatientRecord
        fields = ('record_id', 'username', 'department', 'diagnostics', 'observations', 'treatments', 'misc')
        extra_kwargs = {
            'diagnostics': {'required': True},
            'observations': {'required': True},
            'treatments': {'required': True},
            'misc': {'required': True}
        }

    def get_username(self, obj):
        return obj.patient_id.username

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = customuser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'department')

    def get_department_name(self, obj):
        return obj.department

class RegisterSerializer(serializers.ModelSerializer):
    diagnostics = serializers.CharField(write_only=True, required=False)
    observations = serializers.CharField(write_only=True, required=False)
    treatments = serializers.CharField(write_only=True, required=False)
    misc = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = customuser
        fields = ('id', 'username', 'email', 'password', 'role', 'department', 'diagnostics', 'observations', 'treatments', 'misc')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = customuser.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                role=validated_data['role'],
                department=validated_data['department']
            )
         
        return user