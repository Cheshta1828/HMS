from django.shortcuts import render
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import UserSerializer, PatientRecordSerializer,DepartmentSerializer
from rest_framework.exceptions import PermissionDenied,NotFound
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import RegisterSerializer, UserSerializer
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth.models import Group
from .models import customuser, PatientRecord, Department
from rest_framework.authentication import TokenAuthentication
from django.db import transaction
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.generics import get_object_or_404
from django.views.generic import ListView
from rest_framework.generics import ListCreateAPIView
from .permissions import IsDoctor
from .permissions import IsPatientOrRelevantDoctor,IsRelevantPatientOrDoctor


specialCharacters = "!@#$%^&*_-+=~`|\/:;,.?"




class RegisterAPI(generics.GenericAPIView): 
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):  
        serializer = self.get_serializer(data=request.data)  
        serializer.is_valid(raise_exception=True)

        
        validated_data = serializer.validated_data
        password = validated_data['password']
        role = validated_data['role']

        if len(password) < 8:
            return Response({"error": "password should be greater than 8 characters"}, status=status.HTTP_400_BAD_REQUEST)
        elif (any(char.isalpha() for char in password) == False):
            return Response({"error": "password should contain atleast 1 alphabet"}, status=status.HTTP_400_BAD_REQUEST)
        elif (any(char.isupper() for char in password) == False):
            return Response({"error": "password should contain atleast 1 uppercase letter"}, status=status.HTTP_400_BAD_REQUEST)
        elif (any(char.islower() for char in password) == False):
            return Response({"error": "password should contain atleast 1 lowercase letter"}, status=status.HTTP_400_BAD_REQUEST)
        elif (any(char.isdigit() for char in password) == False):
            return Response({"error": "password should contain atleast 1 digit"}, status=status.HTTP_400_BAD_REQUEST)
        elif all(x not in specialCharacters for x in password):
            return Response({"error": "password should contain atleast 1 special character"}, status=status.HTTP_400_BAD_REQUEST)

        if role == 1:
            
            department = validated_data['department']
            deptins = Department.objects.filter(name__iexact=department)
            if deptins.exists():

                user = customuser.objects.create_user(
                    username=validated_data['username'],
                    email=validated_data['email'],
                    password=validated_data['password'],
                    role=validated_data['role'],
                    department=validated_data['department']
                )
                user_serializer = UserSerializer(user)
                token = default_token_generator.make_token(user)
                group = Group.objects.get(name='Doctors')
                user.groups.add(group)
                print("added to doctor")

                return Response({
                    "user": UserSerializer(user, context=self.get_serializer_context()).data,
                    "token": AuthToken.objects.create(user)[1]
                })
            else:
                raise serializers.ValidationError("Invalid department name")
         

        elif role == 2:
            print("checking for patient")  
            required_fields = ["diagnostics","observations", "treatments", "misc"]
            
            if not set(required_fields).issubset(set(list(validated_data.keys()))):
         
                    return Response({"error": " cannot be blank for a patient."})

                    
            else:
                
                
                    department = validated_data['department']
                    deptins = Department.objects.filter(name__iexact=department)
                    print(deptins)
                    if deptins.exists():
                        idofdept = deptins.first().id
                        print(idofdept)
                        user = customuser.objects.create_user(
                                        username=validated_data['username'],
                                        email=validated_data['email'],
                                        password=validated_data['password'],
                                        role=validated_data['role'],
                                        department=validated_data['department']

                                    )  
                        ins = PatientRecord.objects.create(
                                        patient_id=user,
                                        diagnostics=validated_data['diagnostics'],
                                        observations=validated_data['observations'],
                                        treatments=validated_data['treatments'],
                                        misc=validated_data['misc'],
                                        department=deptins.first()  
                                    )
                        group = Group.objects.get(name='Patients')
                        user.groups.add(group)
                        print("added to patients")
                                    

                        ins.save()

                        token = default_token_generator.make_token(user)
                        user_serializer = UserSerializer(user)
                        

                        return Response({
                                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                                "token": AuthToken.objects.create(user)[1]
                            })
                            
                                    
                    else:
                                
                        return Response({"error":"invalid department name"})



                    
                        
                   
       


class LoginAPI(KnoxLoginView):  

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        print(request.data)
        
        request.data['username'] = request.data['username'].lower()
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)  # Logging in user with the details
        return super(LoginAPI, self).post(request, format=None)








class DoctorsList(generics.ListCreateAPIView):
    permission_classes = [IsDoctor]
    queryset = customuser.objects.filter(role=customuser.DOCTOR)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        role = request.data.get('role')
        if role != 1:
            return Response({"error": "Role should be 1 (Doctor) for creating a doctor."}, status=status.HTTP_400_BAD_REQUEST)

        
        request_data = {
            'username': request.data.get('username'),
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'role': role,
            'department': request.data.get('department')
        }

        
        register_serializer = RegisterSerializer(data=request_data)
        if register_serializer.is_valid():
            user = register_serializer.save()
            group = Group.objects.get(name='Doctors')
            user.groups.add(group)

            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1]
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated, IsDoctor])
def DoctorDetail(request, pk):
    try:
       
        if not request.user.groups.filter(name='Doctors').exists() or request.user.role != customuser.DOCTOR:
            return Response({"error": "Access forbidden. Only doctors are allowed to access this endpoint."}, status=status.HTTP_403_FORBIDDEN)

        
        doctor = customuser.objects.get(pk=pk)

        
        if not doctor.groups.filter(name='Doctors').exists() or doctor.role != customuser.DOCTOR:
            return Response({"error": "The requested user is not a doctor."}, status=status.HTTP_400_BAD_REQUEST)

        
        if request.user.id != doctor.id:
            return Response({"error": "You can only access your own profile."}, status=status.HTTP_403_FORBIDDEN)

        
        if request.method == 'GET':
            serializer = UserSerializer(doctor)
            return Response(serializer.data)

        
        elif request.method == 'PUT':
           
            if request.user.id != doctor.id:
                return Response({"error": "You can only update your own profile."}, status=status.HTTP_403_FORBIDDEN)

            
            if set(request.data.keys()) - {'username', 'email'}:
                return Response({"error": "Only 'username' and 'email' fields can be updated."}, status=status.HTTP_400_BAD_REQUEST)

            
            new_username = request.data.get('username')
            if new_username and customuser.objects.exclude(pk=pk).filter(username=new_username.lower()).exists():
                return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

           
            request.data.pop('password', None)

            serializer = UserSerializer(doctor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        elif request.method == 'DELETE':
            
            if request.user.id != doctor.id:
                return Response({"error": "You can only delete your own profile."}, status=status.HTTP_403_FORBIDDEN)

            doctor.delete()
            return Response({"message": "Doctor deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    except customuser.DoesNotExist:
        return Response({"error": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)
class PatientList(ListCreateAPIView):
    permission_classes = [IsDoctor]
    serializer_class = UserSerializer

    def get_queryset(self):
        
        if self.request.user.role == customuser.DOCTOR:
            
            return customuser.objects.filter(role=customuser.PATIENT, is_superuser=False)
        else:
            return customuser.objects.none()

    def list(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='Doctors').exists() or request.user.role != customuser.DOCTOR:
            return Response({"error": "Access forbidden. Only doctors are allowed to view the list of patients."}, status=status.HTTP_403_FORBIDDEN)

        queryset = self.get_queryset()
        data = []
        for patient in queryset:
            data.append({
                "id": patient.id,
                "username": patient.username,
                "email": patient.email,
                "department": patient.department if patient.department else None,
            })

        return Response(data)

    def create(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='Doctors').exists() or request.user.role != customuser.DOCTOR:
            return Response({"error": "Access forbidden. Only doctors are allowed to create patients."}, status=status.HTTP_403_FORBIDDEN)

        
        username = request.data.get('username')
        email = request.data.get('email')
        department_name = request.data.get('department')
        deptins = Department.objects.filter(name__iexact=department_name)
        print(deptins)
        if deptins.exists():
                    idofdept = deptins.first().id
                    print(idofdept)


        if not (username and email):
            return Response({"error": "Username and email are required fields."}, status=status.HTTP_400_BAD_REQUEST)

        
        if customuser.objects.filter(username=username.lower()).exists():
            return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

        
        request.data['role'] = customuser.PATIENT

       
        register_serializer = RegisterSerializer(data=request.data)
        if register_serializer.is_valid():
            user = register_serializer.save()
            group = Group.objects.get(name='Patients')
            user.groups.add(group)

            
            patient_record = PatientRecord.objects.create(
                patient_id=user,
                diagnostics=request.data.get('diagnostics'),
                observations=request.data.get('observations'),
                treatments=request.data.get('treatments'),
                department=deptins.first(),
                misc=request.data.get('misc')
            )

            data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "department": department_name,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def PatientDetail(request, pk):
    try:
        
        patient = customuser.objects.get(pk=pk)

        
        if request.user.role == customuser.PATIENT:
            
            if request.user.id != patient.id:
                return Response({"error": "Access forbidden. You are not allowed to access this patient's details."},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            
            if request.user.department != patient.department:
                return Response({"error": "Access forbidden. You are not allowed to access this patient's details."},
                                status=status.HTTP_403_FORBIDDEN)

        if request.method == 'GET':
            
            patient_data = UserSerializer(patient).data
            return Response(patient_data)

        elif request.method == 'PUT':
            
            if set(request.data.keys()) - {'username', 'email'}:
                return Response({"error": "Only 'username' and 'email' fields can be updated."},
                                status=status.HTTP_400_BAD_REQUEST)

           
            new_username = request.data.get('username')
            if new_username and customuser.objects.exclude(pk=pk).filter(username=new_username.lower()).exists():
                return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

            
            serializer = UserSerializer(patient, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Patient updated successfully.",
                                                 "updated data":serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            
            patient.delete()
            return Response({"message": "Patient deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    except customuser.DoesNotExist:
        return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)
class PatientRecordsList(ListCreateAPIView):
    permission_classes = [IsDoctor]
    serializer_class = PatientRecordSerializer

    def get_queryset(self):
        
        if self.request.user.role == customuser.DOCTOR:
            return PatientRecord.objects.filter(department__name=self.request.user.department)
        else:
            return PatientRecord.objects.none()

    def post(self, request, *args, **kwargs):
        
        if not request.user.groups.filter(name='Doctors').exists() or request.user.role != customuser.DOCTOR:
            return Response({"error": "Access forbidden. Only doctors are allowed to create patients."},
                            status=status.HTTP_403_FORBIDDEN)

        diagnostics = request.data.get('diagnostics')
        observations = request.data.get('observations')
        treatments = request.data.get('treatments')
        misc = request.data.get('misc')
        department_name = request.data.get('department')
        patient_username = request.data.get('username')

        if not (diagnostics and observations and treatments and misc and department_name and patient_username):
            return Response({"error": "All fields (diagnostics, observations, treatments, misc, department, username) are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        
        try:
            department = Department.objects.get(name=department_name)
        except Department.DoesNotExist:
            return Response({"error": "Invalid department name."},
                            status=status.HTTP_400_BAD_REQUEST)

        
        try:
            patient = customuser.objects.get(username=patient_username)
            if patient.role != customuser.PATIENT:
                raise NotFound("No such patient exists.")
        except customuser.DoesNotExist:
            raise NotFound("No such patient exists.")

        
        if department_name != request.user.department:
            return Response({"error": "You can only create patient records for patients in your department."},
                            status=status.HTTP_403_FORBIDDEN)

        
        patient_record = PatientRecord.objects.create(
            patient_id=patient,
            diagnostics=diagnostics,
            observations=observations,
            treatments=treatments,
            misc=misc,
            department=department
        )

        data = {
            "record_id": patient_record.record_id,
            "patient_id": patient.id,
            "diagnostics": patient_record.diagnostics,
            "observations": patient_record.observations,
            "treatments": patient_record.treatments,
            "misc": patient_record.misc,
            "department": department_name,
        }

        return Response({"message ":"created successfully ","record  is ":data,"status":status.HTTP_201_CREATED})
    



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated,IsRelevantPatientOrDoctor])
def patient_record_detail(request, pk):
    try:
        patient_record = PatientRecord.objects.get(pk=pk)

        
        if request.user.role == customuser.PATIENT:
            
            if request.user != patient_record.patient_id:
                return Response({"error": "Access forbidden. You are not allowed to access this patient record."},
                                status=status.HTTP_403_FORBIDDEN)

        if request.method == 'GET':
            serializer = PatientRecordSerializer(patient_record)
            return Response(serializer.data)

        elif request.method == 'PUT':
            # Only 'diagnostics', 'observations', 'treatments', 'misc' fields can be updated
            serializer = PatientRecordSerializer(patient_record, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            patient_record.delete()
            return Response({"message": "Patient record deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    except PatientRecord.DoesNotExist:
        return Response({"error": "Patient record not found."}, status=status.HTTP_404_NOT_FOUND)
class DepartmentsListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def create(self, request, *args, **kwargs):
        department_name = request.data.get('name')

        if department_name:
            
            existing_department = Department.objects.filter(name__iexact=department_name).first()

            if existing_department:
                return Response({"error": f"Department with name '{department_name}' already exists."},
                                status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

class DepartmentDoctorsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,IsDoctor]

    def get_queryset(self):
        
        if not self.request.user.groups.filter(name='Doctors').exists() or self.request.user.role != customuser.DOCTOR:
            return customuser.objects.none()

        
        department_id = self.kwargs.get('pk')

        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            raise NotFound("No such department exists.")  

        
        if self.request.user.department != department.name:
            raise PermissionDenied("You are only allowed to access your department's records.")

        
        return customuser.objects.filter(role=customuser.DOCTOR, department=department.name)
class DepartmentPatientsView(generics.ListAPIView, generics.UpdateAPIView):
    serializer_class = PatientRecordSerializer
    permission_classes = [permissions.IsAuthenticated,IsDoctor]

    def get_queryset(self):
        
        if not self.request.user.groups.filter(name='Doctors').exists() or self.request.user.role != customuser.DOCTOR:
            return PatientRecord.objects.none()

        
        department_id = self.kwargs.get('pk')

        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            raise NotFound("No such department exists.") 

        
        if self.request.user.department != department.name:
            raise PermissionDenied("You are only allowed to access your department's records.")

        
        return PatientRecord.objects.filter(department=department)

    def get_object(self):
        
        department_id = self.kwargs.get('pk')

        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            raise NotFound("No such department exists.")  

        
        if not self.request.user.groups.filter(name='Doctors').exists() or self.request.user.role != customuser.DOCTOR or self.request.user.department != department.name:
            raise PermissionDenied("You are only allowed to update patient records in your department.")

        
        record_id = self.kwargs.get('record_id')

        try:
            patient_record = PatientRecord.objects.get(pk=record_id)
        except PatientRecord.DoesNotExist:
            raise NotFound("No such patient record exists.")   

        return patient_record