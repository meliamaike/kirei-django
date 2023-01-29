from django.db import models
from services.models import Service
from products.models import Product
from professionals.models import Professional
from payments.models import Payment
from customers.models import Customer


class ShoppingCart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ShoppingCartProduct', through_fields=('shopping_cart','product'))
    services = models.ManyToManyField(Service, through='ShoppingCartServiceDetail', through_fields=('shopping_cart','service'))
    total_amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class ShoppingCartProduct(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class ShoppingCartServiceDetail(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    professional = models.ForeignKey(Professional,on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()

class Reservation(models.Model):
    shopping_cart = models.OneToOneField(ShoppingCart, on_delete=models.CASCADE, blank=False, null=False)
    date_time = models.DateTimeField()
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, blank=True, null=True)
    RESERVATION_STATUS = (
    ('pending', 'Pendiente de pago'),
    ('confirmed', 'Confirmado'),
    ('cancelled', 'Cancelado'),
    ('completed', 'Completado'),
)
    status = models.CharField(max_length=255, choices=RESERVATION_STATUS)

