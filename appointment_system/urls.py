from django.urls import path
from .views import  (login_view, home_view, signup_view, adminSignUp_view, patientSignUp_view, doctorSignUp_view, LogoutView, all_doctor_list, 
all_admin_list, patient_details, doctor_details,
userUpdateView, userpasswordUpdateView, adminUpdateView, delete_user,change_manager_view, patient_update_view, doctor_update_view,
appointment_create, appointment_view_all, report_create_view,view_report, change_appointment, delete_appointment, show_all_appointments
)
from django.conf import settings
app_name =  'appointment_system'

urlpatterns = [
    path('login/',login_view, name="login"),
    path('home/',home_view, name ='home'),
    path('sign-up/',signup_view, name='signup'),
    path('admin/sign-up/',adminSignUp_view),
    path('patient/sign-up/',patientSignUp_view),
    path('doctor/sign-up/',doctorSignUp_view),
    path('logout/',LogoutView.as_view(next_page = settings.LOGOUT_REDIRECT_URL)),
    path('doctor/all/',all_doctor_list),
    path('admin/all/',all_admin_list),
    path('patient/details/',patient_details),
    path('doctor/details/',doctor_details),
    path('user/update/',userUpdateView),
    path('user/password/',userpasswordUpdateView),
    path('admin/update/', adminUpdateView, name='admin_update'),
    path('user/delete/',delete_user),
    path('admin/change-manager/<int:pk>',change_manager_view,name='change_manager'),
    path('patient/update/',patient_update_view),
    path('doctor/update/',doctor_update_view),
    path('appointment/create/',appointment_create),
    path('doctor/appointments/',appointment_view_all),
    path('report/create/<int:pk>',report_create_view ,name='create_report'),
    path('report/view/',view_report),
    path('appointment/update/<int:pk>',change_appointment, name='change_appointment'),
    path('appointment/delete/<int:pk>',delete_appointment, name='cancel_appointment'),
    path('appointment/all/',show_all_appointments),

]
