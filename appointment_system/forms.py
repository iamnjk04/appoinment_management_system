from django import forms
from django.contrib.auth import get_user_model
from django.forms import fields
from .models import Admin, Doctor, Patient, Appointment, Report
from django.contrib.auth.forms import PasswordChangeForm, ReadOnlyPasswordHashField, UserChangeForm

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())


class SignUpForm(forms.Form):
    # first_name = forms.CharField(max_length=30)
    # last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    age = forms.IntegerField()

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError('This User name is Taken')
        return self.cleaned_data['username']

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password Must be Same.")

class AdminSignUpForm(forms.ModelForm):
    class Meta:
        fields = ['admin_rank',]
        model = Admin

class PatientSignUpForm(forms.ModelForm):
    class Meta:
        fields = ['patient_gender','blood_group',]
        model = Patient

class DoctorSignUpForm(forms.ModelForm):
    class Meta:
        fields = ['doctor_qualification','nmc_number','doctor_field']
        model = Doctor

class UserUpdateForm(UserChangeForm):
    # password = forms.CharField(widget=forms.PasswordInput)
    password = None
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('username','email','age')
        # exclude = ['groups','user_permissions','password']

class ChangeManagerForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('managed_by',)


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('appointment_date','appointment_details','doctor')

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('prescription_name','report_details')