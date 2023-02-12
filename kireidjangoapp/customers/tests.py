# from django.test import TestCase

# from django.test import TestCase
# from customers.models import Customer
# from django.contrib.auth.hashers import make_password


# class CustomerModelTest(TestCase):
#     def test_check_password(self):
#         # create a new customer
#         customer = Customer.objects.create(
#             first_name="Mel",
#             last_name="Ama",
#             email="crazy@hot.com",
#             document_type="dni",
#             document_number="344534534",
#             country_code="45",
#             area_code="11",
#             phone_number="+54354354355",
#             password=make_password("meliama95"),
#         )
#         # set password for customer
#         customer.save()
#         # check if password matches
#         self.assertTrue(customer.check_password("meliama95"))
#         self.assertFalse(customer.check_password("wrongpassword"))
