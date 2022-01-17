from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin  as BaseUserAdmin
from .forms_admin import UserAdminCreationForm, UserAdminChangeForm
from .models import Admin,Appointment, Doctor, Patient,Report
# from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

admin.site.unregister(Group)
# admin.site.register(User)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['username', 'is_doctor', 'is_superuser']
    list_filter = ['is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ('username','first_name','last_name','age',)}),
        ('Permissions', {'fields': ('is_doctor','is_staff','is_active','is_superuser','last_login','date_joined',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2','username','first_name','last_name','age','is_staff','is_active','is_superuser','last_login','date_joined','is_doctor',)}
        ),
    )
    search_fields = ['email','username']
    ordering = ['email']
    filter_horizontal = ()

# admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Admin)
admin.site.register(Appointment)
admin.site.register(Doctor)
# admin.site.register(Doctor_Schedule)
admin.site.register(Patient)
admin.site.register(Report)
