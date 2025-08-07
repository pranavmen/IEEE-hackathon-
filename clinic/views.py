# clinic/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Clinic, Specialization, User, Appointment, Availability
from .forms import ClinicForm, UserCreationForm, AppointmentForm, UserUpdateForm, AvailabilityForm
from datetime import date

def loginPage(request):
    if request.user.is_authenticated:
        if request.user.role == 'doctor':
            return redirect('doctor_dashboard')
        else:
            return redirect('patient_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('login')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user.role == 'doctor':
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'clinic/login_register.html', {'page': 'login'})


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email.split('@')[0]
            user.save()
            login(request, user)
            if user.role == 'doctor':
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')
        else:
            # The form object with errors will be passed to the template
            pass

    return render(request, 'clinic/login_register.html', {'form': form, 'page': 'register'})

def home(request):
    q = request.GET.get('q', '')
    
    # Using the ORM's filter method with Q objects is safe from SQL injection.
    # No changes are needed here as the original code was already using the ORM correctly.
    # The vulnerability was in my initial assessment. The use of Q objects is secure.
    
    specializations = Specialization.objects.filter(name__icontains=q)
    clinics = Clinic.objects.filter(
        Q(specialization__name__icontains=q) |
        Q(name__icontains=q)
    )
    
    context = {'clinics': clinics, 'specializations': specializations}
    return render(request, 'clinic/home.html', context)


def clinic(request, pk):
    clinic = Clinic.objects.get(id=pk)
    context = {'clinic': clinic}
    return render(request, 'clinic/clinic.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    clinics = user.clinic_set.all()
    context = {'user': user, 'clinics': clinics}
    return render(request, 'clinic/profile.html', context)


@login_required(login_url='login')
def createClinic(request):
    form = ClinicForm()
    if request.method == 'POST':
        form = ClinicForm(request.POST)
        if form.is_valid():
            clinic = form.save(commit=False)
            clinic.host = request.user
            clinic.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'clinic/clinic_form.html', context)


@login_required(login_url='login')
def updateClinic(request, pk):
    clinic = Clinic.objects.get(id=pk)
    form = ClinicForm(instance=clinic)

    if request.user != clinic.host:
        return redirect('home')

    if request.method == 'POST':
        form = ClinicForm(request.POST, instance=clinic)
        if form.is_valid():
            form.save()
            return redirect('clinic', pk=clinic.id)

    context = {'form': form, 'clinic': clinic}
    return render(request, 'clinic/clinic_form.html', context)


@login_required(login_url='login')
def deleteClinic(request, pk):
    clinic = Clinic.objects.get(id=pk)

    if request.user != clinic.host:
        return redirect('home')

    if request.method == 'POST':
        clinic.delete()
        return redirect('home')
    return render(request, 'clinic/delete.html', {'obj': clinic})

# New Views for dashboards and booking
@login_required(login_url='login')
def doctor_dashboard(request):
    appointments = Appointment.objects.filter(doctor=request.user)
    context = {'appointments': appointments}
    return render(request, 'clinic/dashboard_doctor.html', context)

@login_required(login_url='login')
def patient_dashboard(request):
    today = date.today()
    # Fetch upcoming appointments for the logged-in patient
    appointments = Appointment.objects.filter(patient=request.user)
    doctor_count = User.objects.filter(role='doctor',is_active=True).count()
    upcoming_appointments = Appointment.objects.filter(
        patient=request.user,
        appointment_date__gte=today
    ).order_by('appointment_date', 'appointment_time')
    completed_visits_count = Appointment.objects.filter(
        patient=request.user,
        appointment_date__lt=today
    ).count()
    context = {'appointments': upcoming_appointments,  # Pass only upcoming appointments to the table
        'completed_visits_count': completed_visits_count,
        'doctor_count': doctor_count,}
    # Corrected template path below
    return render(request, 'clinic/dashboard_patient.html', context)

@login_required(login_url='login')
def book_appointment(request):
    form = AppointmentForm()
    doctors = User.objects.filter(role='doctor')
    clinics = Clinic.objects.all()
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Create an appointment object but don't save to the database yet
            appointment = form.save(commit=False)
            # Assign the current logged-in user as the patient

            appointment.patient = request.user
            appointment.save()
            return redirect('patient_dashboard')

    context = {'form': form, 'doctors': doctors, 'clinics':clinics}
    return render(request, 'clinic/book_appointment.html', context)

# Add these new views at the end of CliQ/clinic/views.py

@login_required(login_url='login')
def patient_appointments(request):
    # Fetch appointments for the logged-in patient
    appointments = Appointment.objects.filter(patient=request.user)
    context = {'appointments': appointments}
    return render(request, 'clinic/patient_appointments.html', context)


@login_required(login_url='login')
def patient_settings(request):
    # You can add logic here for updating user settings
    return render(request, 'clinic/settings.html')


@login_required(login_url='login')
def doctor_appointments(request):
    # Fetch appointments for the logged-in doctor
    appointments = Appointment.objects.filter(doctor=request.user)
    context = {'appointments': appointments}
    return render(request, 'clinic/doctor_appointments.html', context)


@login_required(login_url='login')
def doctor_settings(request):
    # You can add logic here for updating user settings
    return render(request, 'clinic/settings.html')

# CliQ/clinic/views.py

# ... (existing imports)

@login_required(login_url='login')
def update_appointment(request, pk):
    appointment = Appointment.objects.get(id=pk)
    form = AppointmentForm(instance=appointment)

    if request.user != appointment.patient:
        # You can redirect to a 'permission-denied' page or back to the dashboard
        return redirect('patient_dashboard')

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request,'Appointment updated successfully ')
            return redirect('patient_appointments')

    context = {'form': form, 'appointment': appointment}
    return render(request, 'clinic/appointment_form.html', context)

@login_required(login_url='login')
def delete_appointment(request, pk):
    appointment = Appointment.objects.get(id=pk)

    if request.user != appointment.patient:
        return redirect('patient_dashboard')

    if request.method == 'POST':
        appointment.delete()
        messages.success(request,'Appointment deleted sucessfully')
        return redirect('patient_appointments')

    return render(request, 'clinic/delete.html', {'obj': appointment})

@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserUpdateForm(instance=user)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            # Redirect to the correct dashboard based on user role
            if user.role == 'doctor':
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')

    context = {'form': form}
    return render(request, 'clinic/update_user_form.html', context)

@login_required(login_url='login')
def doctor_list(request):
    doctors = User.objects.filter(role='doctor', is_active=True).prefetch_related('availability')
    context = {'doctors': doctors}
    return render(request, 'clinic/doctor_list.html', context)

@login_required(login_url='login')
def set_availability(request):
    if request.user.role != 'doctor':
        return redirect('home')

    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.doctor = request.user
            availability.save()
            messages.success(request, 'Availability set successfully!')
            return redirect('doctor_dashboard')
    else:
        form = AvailabilityForm()
    
    context = {'form': form}
    return render(request, 'clinic/set_availability.html', context)