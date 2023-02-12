from django.contrib.auth.backends import ModelBackend, BaseBackend
from django.contrib.auth import get_user_model
from django.db.models.query_utils import Q
from customers.models import Customer


UserModel = Customer

class EmailOrUsernameModelBackend(BaseBackend):
    
    def authenticate(request,username=None, password=None):
        try:
            user = UserModel.objects.get(Q(username=username) | Q(email=username))
            print("antes check_password:", user)

            if user.my_check_password(raw_password=password):
                print("dsp del check_password",user)
                print(user)
                return user
        except UserModel.DoesNotExist:
            None
    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


