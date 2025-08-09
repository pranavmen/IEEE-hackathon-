from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Specialization(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Clinic(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    doctors = models.ManyToManyField(User, related_name='clinics', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Availability(models.Model):
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availability')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('doctor', 'day',)

    def __str__(self):
        return f"Dr. {self.doctor.name}'s availability on {self.day}"


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, name='Specialization')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    appointment_datetime = models.DateTimeField()
    reason = models.TextField(max_length=500)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Scheduled')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        formatted_time = self.appointment_datetime.strftime("%d %b %Y, %I:%M %p")
        return f"Appointment for {self.patient.name} with Dr. {self.doctor.name} on {formatted_time}"

    class Meta:
        ordering = ['-appointment_datetime']
        unique_together = ('doctor', 'appointment_datetime')