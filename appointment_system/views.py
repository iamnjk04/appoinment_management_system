from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import query
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import (LoginForm, SignUpForm, AdminSignUpForm, PatientSignUpForm, DoctorSignUpForm,
 UserUpdateForm,ChangeManagerForm, AppointmentForm, ReportForm)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, update_session_auth_hash

from .models import Admin, Appointment, Doctor, Patient, Report


from django.contrib.auth.views import LogoutView
USER =  get_user_model()

def login_view(request):
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print(request.POST)
            print(form.cleaned_data)
            print(form.cleaned_data['username'])
            # authentication of the user model
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user:
                print(user, '<--- USER OBJECT')
                print(type(user))
                login(request,user=user)
            return redirect('/appointmentx/home/')
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/appointmentx/home/')
            # pass
        form = LoginForm()
    return render(request, 'appointment_system/login.html',{'form':form})

@login_required
def home_view(request):
    query = None
    if request.user.is_superuser:
        query = Doctor.objects.filter(managed_by = None)
    elif (not request.user.is_superuser ) and (not request.user.is_doctor):
        query = Appointment.objects.filter(is_reported = False)
    return render(request, 'appointment_system/dashboard.html',{'context':query})

def signup_view(request):
    if request.method =="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("FOrm is Valid")
            print(form.cleaned_data)
            # Importing the User Model
            user = USER(
                username = form.cleaned_data['username'],
                # first_name = form.cleaned_data['first_name'],
                # last_name = form.cleaned_data['last_name'],
                password = form.cleaned_data['password'],
                age = form.cleaned_data['age']
            )
            user.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('/appointmentx/login/')
    elif request.method =='GET':
        form = SignUpForm()
    return render(request, 'appointment_system/login.html',{'form':form})


def adminSignUp_view(request):
    if request.method =='POST':
        form1 = SignUpForm(request.POST)
        form2 = AdminSignUpForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            # print("FOrm is Valid")
            # print(form.cleaned_data)
            # Importing the User Model
            user = USER(
                email = form1.cleaned_data['email'],
                username = form1.cleaned_data['username'],
                password = form1.cleaned_data['password'],
                age = form1.cleaned_data['age'],
                is_superuser = True,
                is_staff = True
            )
            user.save()
            user.set_password(form1.cleaned_data['password'])
            user.save()
            Admin.objects.create(admin =user, admin_rank = form2.cleaned_data['admin_rank'])
            return redirect('/appointmentx/login/')
    elif request.method == 'GET':
        form1 = SignUpForm
        form2 = AdminSignUpForm
    return render(request, 'appointment_system/signup.html',{'form1':form1, 'form2':form2})




def patientSignUp_view(request):
    if request.method =='POST':
        form1 = SignUpForm(request.POST)
        form2 = PatientSignUpForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            # print("FOrm is Valid")
            # print(form.cleaned_data)
            # Importing the User Model
            user = USER(
                email = form1.cleaned_data['email'],
                username = form1.cleaned_data['username'],
                # first_name = form.cleaned_data['first_name'],
                # last_name = form.cleaned_data['last_name'],
                password = form1.cleaned_data['password'],
                age = form1.cleaned_data['age'],
            )
            user.save()
            user.set_password(form1.cleaned_data['password'])
            user.save()
            blood_group = form2.cleaned_data['blood_group']
            patient_gender = form2.cleaned_data['patient_gender']
            Patient.objects.create(patient=user, patient_gender=patient_gender,blood_group=blood_group )
            return redirect('/appointmentx/login/')
    elif request.method == 'GET':
        form1 = SignUpForm
        form2 = PatientSignUpForm
    return render(request, 'appointment_system/signup.html',{'form1':form1, 'form2':form2})

@login_required
def doctorSignUp_view(request):
    if request.method =='POST':
        form1 = SignUpForm(request.POST)
        form2 = DoctorSignUpForm(request.POST)
        if form1.is_valid() and form2.is_valid() and request.user.is_superuser:
            # print("FOrm is Valid")
            # print(form.cleaned_data)
            # Importing the User Model
            user = USER(
                email = form1.cleaned_data['email'],
                username = form1.cleaned_data['username'],
                # first_name = form.cleaned_data['first_name'],
                # last_name = form.cleaned_data['last_name'],
                password = form1.cleaned_data['password'],
                age = form1.cleaned_data['age'],
                is_doctor = True
            )
            # nmc_number = form2.cleaned_data['nmc_number']
            # doctor_qualification = form2.cleaned_data['doctor_qualification']
            user.save()
            user.set_password(form1.cleaned_data['password'])
            user.save()
            # customer new datas --address and date
            doctor_form = form2.save(commit = False)
            doctor_form.managed_by = request.user
            doctor_form.doctor = user
            doctor_form.save()
            # registered =True
            # Doctor.objects.create(doctor=request.user, doctor_qualification=doctor_qualification,nmc_number=nmc_number )
            return redirect('/appointmentx/login/')
        else:
            pass
    elif request.method == 'GET':
        form1 = SignUpForm
        form2 = DoctorSignUpForm
    return render(request, 'appointment_system/signup.html',{'form1':form1, 'form2':form2})

def all_doctor_list(request):
    query = Doctor.objects.all()
    return render(request,'appointment_system/list_details.html',{'context':query})


def all_admin_list(request):
    query = Admin.objects.all()
    return render(request,'appointment_system/admin_list_details.html',{'context':query})

def patient_details(request):
    user_ = USER.objects.get(username = request.user.username)
    query = Patient.objects.get(patient = user_)
    print(query)
    # query = Patient.objects.filter(patient = request.user)
    return render(request,'appointment_system/details.html',{'context':query})

def doctor_details(request):
    user_ = USER.objects.get(username = request.user.username)
    query = Doctor.objects.get(doctor = user_)
    return render(request,'appointment_system/details.html',{'context':query})

@login_required
def userUpdateView(request):
    if request.method =="POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/appointmentx/home/')
    elif request.method =='GET':
        form = UserUpdateForm(instance=request.user)
    return render(request, 'appointment_system/user_update.html',{'form':form})

@login_required
def adminUpdateView(request):
    if request.method =='POST':
        form1 = UserUpdateForm(request.POST, instance=request.user)
        form2 = AdminSignUpForm(request.POST, instance=request.user.admin)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('/appointmentx/home/')
    else:
        form1 = UserUpdateForm(instance = request.user)
        form2 = AdminSignUpForm(instance=request.user.admin)
    return render(request,'appointment_system/signup.html',{'form1':form1, 'form2':form2})

@login_required
def userpasswordUpdateView(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            # messages.success(request, 'Your password was successfully updated!')
            return redirect('/appointmentx/home')
        # else:
        #     messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'appointment_system/user_update.html', {
        'form': form
    })

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    USER.objects.get(username = user.username).delete()
    return redirect('/appointmentx/login/')

@login_required
def change_manager_view(request, pk):
    doc = Doctor.objects.get(id =pk)
    if request.method == 'POST':
        form = ChangeManagerForm(request.POST, instance=doc)
        if form.is_valid():
            form.save()
            return redirect('/appointmentx/home')

    else:
        form = ChangeManagerForm(instance = doc)
    return render(request, 'appointment_system/user_update.html', {
        'form': form
    })
    # return render(request, 'appointment_system/user_update.html')
@login_required
def patient_update_view(request):
    if request.method =='POST':
        form1 = UserUpdateForm(request.POST, instance=request.user)
        form2 = PatientSignUpForm(request.POST, instance=request.user.patient)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('/appointmentx/home/')
    else:
        form1 = UserUpdateForm(instance = request.user)
        form2 = PatientSignUpForm(instance=request.user.patient)
    return render(request,'appointment_system/signup.html',{'form1':form1, 'form2':form2})


@login_required
def doctor_update_view(request):
    if request.method =='POST':
        form1 = UserUpdateForm(request.POST, instance=request.user)
        form2 = DoctorSignUpForm(request.POST, instance=request.user.doctor)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('/appointmentx/home/')
    else:
        form1 = UserUpdateForm(instance = request.user)
        form2 = DoctorSignUpForm(instance=request.user.doctor)
    return render(request,'appointment_system/signup.html',{'form1':form1, 'form2':form2})

@login_required
def appointment_create(request):
    if request.method =='POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            Appointment.objects.create(patient = request.user.patient, 
            appointment_date = form.cleaned_data['appointment_date'],
            appointment_details = form.cleaned_data['appointment_details'],
            doctor = form.cleaned_data['doctor']
            )
            return redirect('/appointmentx/home/')
    else:
        form = AppointmentForm
    return render(request, 'appointment_system/user_update.html',{'form':form})


def appointment_view_all(request):
    query = Appointment.objects.filter(doctor = request.user.doctor,is_reported = False)
    return render(request, 'appointment_system/admin_list_details.html',{'context':query})

@login_required
def report_create_view(request, pk):
    if request.method =='POST':
        form = ReportForm(request.POST)
        app = Appointment.objects.get(id = pk)
        if form.is_valid():
            Report.objects.create(
                prescription_name = form.cleaned_data['prescription_name'],
                report_details = form.cleaned_data['report_details'],
                appointment = app,
                doctor_name = request.user.doctor
            )
        app.is_reported = True
        app.save()
        return redirect('/appointmentx/home/')
    else:
        form = ReportForm
    return render(request,'appointment_system/user_update.html',{'form':form})   

@login_required
def view_report(request):
    query = Appointment.objects.filter(patient = request.user.patient, is_reported = True)
    return render(request, 'appointment_system/admin_list_details.html',{'context':query})

@login_required
def change_appointment(request,pk):
    app = Appointment.objects.get(id = pk)
    if request.method =="POST":
        form = AppointmentForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
        # app.is_reported = True
        return redirect('/appointmentx/home/')
    else:
        form = AppointmentForm(instance=app)
    return render(request,'appointment_system/user_update.html',{'form':form})

@login_required
def delete_appointment(request, pk):
    # We can keep into both REQUEST.POST as well as REQUEST.GET as well
    # if request.method =="GET":
    obj =  get_object_or_404(Appointment, id=pk)
    obj.delete()
    return redirect('/appointmentx/home/')

@login_required
def show_all_appointments(request):
    query = Appointment.objects.all().order_by('appointment_date')
    return render(request, 'appointment_system/appointment_details.html',{'context':query})
 