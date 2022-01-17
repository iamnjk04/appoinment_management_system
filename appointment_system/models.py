from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USERNAME_FIELD = 'username'
    is_doctor = models.BooleanField(default=False)
    age =  models.PositiveIntegerField(null=True,blank=True)
    groups = None
    user_permissions = None

    def __str__(self):
        return self.username
    # proxy =  True

class Patient(models.Model):
    gender_choices = [
        ('M', 'Male'),
        ('F','Female'),
        ('O', 'Others')
    ]  
    blood_group_choices = [
        ('A+','A positive'),
        ('A-','A negative'),
        ('B+','B positive'),
        ('B-','B negative'),
        ('AB+','AB positive'),
        ('AB-','AB negative'),
        ('O+','O positive'),
        ('O-', 'O negative'),
    ]
    patient_gender =  models.CharField(choices=gender_choices, max_length=2)
    blood_group = models.CharField(choices=blood_group_choices, max_length=4)
    patient = models.OneToOneField(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
    
    # def __str__(self): 
    #     return self.patient

class Admin(models.Model):
    rank_choices = [
        ('Manager', 'Manager'),
        ('Director','Director'),
        ('Database Manager', 'Database Manager'),
    ]
    admin_rank = models.CharField(choices=rank_choices, max_length=18)
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'
    def __str__(self):
        return self.admin.username
    

class Doctor(models.Model):
    nmc_number = models.PositiveIntegerField()
    qualification_choice = [
        ('M.D.','Masters'),
        ('M.B.B.S','Bachelor'),
        ('P.H.D','Doctorate'),
    ]
    doctor_field = models.CharField(max_length=100)
    doctor_qualification = models.CharField(choices=qualification_choice, max_length=8)
    managed_by =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='admin_of')
    doctor = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors' 
    def __str__(self):
        return f'Dr. {self.doctor.username} Specialist in {self.doctor_field}'


class Appointment(models.Model):
    appointment_date = models.DateField()
    appointment_details = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL , null=True)
    is_reported = models.BooleanField(default=False)

class Report(models.Model):
    prescription_name = models.CharField(max_length=200)
    report_details = models.TextField()
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    doctor_name = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)    

# class Doctor_Schedule(models.Model):
#     day_choice =  [
#         ('6',"Sunday"),
#         ('0',"Monday"),
#         ('1',"Tuesday"),
#         ('2',"Wednesday"),
#         ('3',"Thursday"),
#         ('4',"Friday"),
#         ('5',"Saturday"),
#     ]
#     ds_day = models.CharField(choices=day_choice, max_length=10)
#     ds_time = models.TimeField()
#     doctor =  models.ForeignKey(Doctor, on_delete=models.CASCADE)





