from django.db import models
from shoppingcarts.models import Reservation
from products.models import Product
from services.models import Service
from customers.models import Customer


"""
    Modelo "Pago": Este modelo tendría campos como monto, fecha, 
    forma de pago, y reserva de la cita asociada.
"""
    
class Payment(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    transaction_number = models.CharField(max_length=255, unique=True)
    PAYMENT_METHOD = (
    ('credit_card', 'Tarjeta de crédito'),
    ('debit_card', 'Tarjeta de débito'),
    ('cash', 'Efectivo'),
    
    ('bank_transfer', 'Transferencia bancaria'),
    ('mercado_pago', 'Mercado Pago'),
    ('other', 'Otro'),
)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHOD)
    PAYMENT_STATUS = (
    ('pending', 'Pendiente'),
    ('success', 'Exitosa'),
    ('failed', 'Fallida'),
    ('refunded', 'Reembolsada'),
    ('cancelled', 'Cancelada'),
)
    status = models.CharField(max_length=255, choices=PAYMENT_STATUS)

"""
    Modelo "Factura": Este modelo tendría campos como fecha, 
    cliente asociado, los productos comprados y 
    servicios comprados, y el monto total.
"""

class Bill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    services = models.ManyToManyField(Service)
    total_amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
