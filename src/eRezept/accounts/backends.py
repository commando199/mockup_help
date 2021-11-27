from django.contrib.auth.backends import BaseBackend
from .models import Praxis, Admin

class MyBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            praxis = Praxis.objects.get(email=email)
            if check_password(password, praxis.password) and praxis.accepted_by_medorg == True:
                praxis_true = praxis
                return praxis_true
            elif check_password(password, praxis.password) and praxis.accepted_by_medorg == False:
                return "not yet validated"
            else:
                return None
        except Praxis.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Praxis.objects.get(pk=user_id)
        except Praxis.DoesNotExist:
            return None

class AdminBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            admin = Admin.objects.get(email=email)
            if check_password(password, admin.password):
                return admin
            else:
                return None
        except Admin.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Admin.objects.get(pk=user_id)
        except Admin.DoesNotExist:
            return None