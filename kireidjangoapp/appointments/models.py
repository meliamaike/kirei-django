from django.db import models
from services.models import Service
from professionals.models import Professional
from customers.models import Customer
from agendas.models import Agenda

# Cita a reservar

class Appointment(models.Model):
    profesional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    

    