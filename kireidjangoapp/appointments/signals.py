import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Agenda, AppointmentSlot


@receiver(post_save, sender=Agenda)
def create_appointment_slots(sender, instance, created, **kwargs):
    if created:
        start_time = datetime.strptime(instance.start_time, "%H:%M").time()
        end_time = datetime.strptime(instance.end_time, "%H:%M").time()
        current_time = start_time
        while current_time < end_time:
            AppointmentSlot.objects.create(
                agenda=instance,
                start_time=current_time,
                end_time=current_time + datetime.timedelta(minutes=15),
                booked=False,
            )
            current_time += datetime.timedelta(minutes=15)
