# HMS API DOCUMENTATION- https://cheshta1828.pythonanywhere.com


                             HMS API Documentation

                             
Table of Contents
1.Authentication
2.Register User
3.Login User
4.Logout User
5.List and Create Doctors
6.Retrieve, Update, and Delete Doctor
7.List and Create Patients
8.Retrieve, Update, and Delete Patient
9.List and Create Patient Records
10.Retrieve, Update, and Delete Patient Record
11.List and Create Departments
12.Retrieve, Update, and Delete Department
13.List Doctors in a Department
14.List Patient Records in a Department

Authentication
All endpoints require authentication using an API token. Use the token in the Authorization header of your requests.
Register User
URL: /register
Method: POST
Description: Register a new user (doctor or patient).
Parameters:
username (string, required): The username for the user.
email (string, required): The email address of the user.
password (string, required): The password for the user.
role (integer, required): Role of the user (1 for doctor, 2 for patient).
department (string, required for doctors): Department name for doctors.
diagnostics (string, optional, required for patients): Initial diagnostics for patients.
observations (string, optional, required for patients): Initial observations for patients.
treatments (string, optional, required for patients): Initial treatments for patients.
misc (string, optional, required for patients): Additional information for patients.
Responses:
201 Created: User registration successful.
400 Bad Request: Invalid or missing parameters.
403 Forbidden: Access forbidden.
Login User
URL: /login
Method: POST
Description: Log in an existing user.
Parameters:
username (string, required): The username of the user.
password (string, required): The password of the user.
Responses:
200 OK: Login successful, returns user token.
400 Bad Request: Invalid or missing parameters.
Logout User
URL: /logout
Method: POST
Description: Log out the authenticated user.
Parameters: None.

Responses:
200 OK: Logout successful.
List and Create Doctors
URL: /doctors/
Method: GET, POST
Description: List all doctors or create a new doctor (Admin/Doctors only).
Parameters: None (for GET).
Responses:
200 OK: Returns a list of doctors (for GET).
201 Created: Doctor creation successful (for POST).
400 Bad Request: Invalid or missing parameters (for POST).
403 Forbidden: Access forbidden.
Retrieve, Update, and Delete Doctor
URL: /doctors/<int:pk>
Method: GET, PUT, DELETE
Description: Retrieve, update, or delete a specific doctor.
Parameters:
pk (integer, required): The ID of the doctor.

Responses:
200 OK: Returns doctor details (for GET).
200 OK: Doctor details updated successfully (for PUT).
204 No Content: Doctor deleted successfully (for DELETE).
400 Bad Request: Invalid or missing parameters.
403 Forbidden: Access forbidden.
List and Create Patients
URL: /patients/
Method: GET, POST
Description: List all patients or create a new patient (Doctors only).
Parameters: None (for GET).
Responses:
200 OK: Returns a list of patients (for GET).
201 Created: Patient creation successful (for POST).
400 Bad Request: Invalid or missing parameters (for POST).
403 Forbidden: Access forbidden.



Retrieve, Update, and Delete Patient
URL: /patients/<int:pk>
Method: GET, PUT, DELETE
Description: Retrieve, update, or delete a specific patient.
Parameters: pk (integer, required): The ID of the patient.
Responses:
200 OK: Returns patient details (for GET).
200 OK: Patient details updated successfully (for PUT).
204 No Content: Patient deleted successfully (for DELETE).
400 Bad Request: Invalid or missing parameters.
403 Forbidden: Access forbidden.
List and Create Patient Records
URL: /patient_records/
Method: GET, POST
Description: List all patient records or create a new patient record (Doctors only).
Parameters: None (for GET).
Responses:
200 OK: Returns a list of patient records (for GET).
201 Created: Patient record creation successful (for POST).
400 Bad Request: Invalid or missing parameters (for POST).
403 Forbidden: Access forbidden.
Retrieve, Update, and Delete Patient Record
URL: /patient_records/<int:pk>
Method: GET, PUT, DELETE
Description: Retrieve, update, or delete a specific patient record.
Parameters:pk (integer, required): The ID of the patient record.
Responses:
200 OK: Returns patient record details (for GET).
200 OK: Patient record details updated successfully (for PUT).
204 No Content: Patient record deleted successfully (for DELETE).
400 Bad Request: Invalid or missing parameters.
403 Forbidden: Access forbidden.
List and Create Departments
URL: /departments/
Method: GET, POST
Description: List all departments or create a new department (Admin/Doctors only).
Parameters: None (for GET).

Responses:
200 OK: Returns a list of departments (for GET).
201 Created: Department creation successful (for POST).
400 Bad Request: Invalid or missing parameters (for POST).
403 Forbidden: Access forbidden.
Get Doctors in a Department
URL: /departments/int:pk/doctors
Method: GET
Permissions: IsDoctor
Description: This endpoint allows authenticated doctors to get a list of all doctors belonging to a specific department.
Request Parameters:pk (integer, required): The primary key of the department.
Responses:
200 OK: Successfully retrieved the list of doctors.
400 Bad Request: Invalid or missing parameters.
403 Forbidden: Access forbidden.



Get Patients' Records in a Department
URL: /departments/int:pk/patients
Method: GET
Permissions: IsDoctor
Description: This endpoint allows authenticated doctors to get a list of patient records belonging to a specific department.
Request Parameters:pk (integer, required): The primary key of the department.
Responses:
200 OK: Successfully retrieved the list of patient records.
400 Bad Request: Invalid or missing parameters.
403 Forbidden: Access forbidden.



