from django.shortcuts import render


# def create_agenda(request):
#     if request.method == 'POST':
#         form = AgendaForm(request.POST)
#         if form.is_valid():
#             agenda = form.save()
#             AppointmentSlot.create_appointment_slots(agenda)
#             return redirect('agenda_detail', agenda.id)
#     else:
#         form = AgendaForm()
#     return render(request, 'create_agenda.html', {'form': form})

