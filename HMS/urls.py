from django.contrib import admin
from django.urls import path
from knox import views as knox_views
from django.urls import path
from django.urls import path
from accounts.views import DoctorsList, DoctorDetail,PatientDetail,patient_record_detail
from accounts.views import LoginAPI , RegisterAPI , DoctorsList,PatientList,PatientRecordsList,DepartmentsListCreateView,DepartmentDoctorsView,DepartmentPatientsView

urlpatterns = [
    path('admin/', admin.site.urls), #admin panel with all the user objects
    path('register', RegisterAPI.as_view(), name='register'), # register user Method is POST
    path('login', LoginAPI.as_view(), name='login'), # login user Method is POST
    path('logout', knox_views.LogoutView.as_view(), name='logout'), # Logout the user Method id POSR
    
    path('doctors/', DoctorsList.as_view(), name='doctors-list'),
     path('doctors/<int:pk>', DoctorDetail, name='doctor-detail'),
     path('patients/',PatientList.as_view(),name='patient-list'),
     path('patients/<int:pk>', PatientDetail, name='patient-detail'),
     path('patient_records/', PatientRecordsList.as_view(), name='patient-record-list'),
     path('patient_records/<int:pk>', patient_record_detail, name='patient-record-detail'),
     path('departments/', DepartmentsListCreateView.as_view(), name='departments-list-create'),
     path('department/<int:pk>/doctors', DepartmentDoctorsView.as_view(), name='department-doctors'),
     path('department/<pk>/patients',DepartmentPatientsView.as_view(),name='department-patients')
]