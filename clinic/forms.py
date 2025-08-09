

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User, Clinic, Appointment, Availability

# This is the new, corrected code
class UserCreationForm(BaseUserCreationForm):
     class Meta(BaseUserCreationForm.Meta):
         model = User
         fields = BaseUserCreationForm.Meta.fields + ('name', 'email', 'role')

        
class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email']

class ClinicForm(ModelForm):
    class Meta:
        model = Clinic
        
        fields = ['specialization', 'name', 'description']

class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['clinic','doctor', 'appointment_datetime' ,'reason']

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)

        self.fields['doctor'].queryset = User.objects.filter(role='doctor')

class AvailabilityForm(ModelForm):
    class Meta:
        model = Availability
        fields = ['day', 'start_time', 'end_time']