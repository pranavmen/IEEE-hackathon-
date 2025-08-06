from django.contrib import admin
from .models import User, Specialization, Clinic, Appointment

# Register your models here.
admin.site.register(User)
admin.site.register(Specialization)
admin.site.register(Clinic)
admin.site.register(Appointment)