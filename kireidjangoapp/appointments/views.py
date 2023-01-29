from django.shortcuts import render

from appointments.models import AppointmentSlot, Appointment


# Create your views here.
# def create_appointment(request):
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             customer = form.cleaned_data['customer']
#             servicio = form.cleaned_data['servicio']
#             profesional = form.cleaned_data['profesional']
#             appointment_slot = AppointmentSlot.create_appointment_slots(agenda=form.cleaned_data['agenda'], start_time=form.cleaned_data['start_time'], end_time=form.cleaned_data['end_time'])
#             Appointment.create_appointment(customer=customer, servicio=servicio, profesional=profesional, appointment_slot=appointment_slot)
#             return redirect('app
