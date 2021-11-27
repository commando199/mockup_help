from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import CustomUser
from .models import  Praxis, ShippingInfo



# form um ärzte zu registrieren.
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'vorname', 'nachname',
                  'anrede', 'praxis_name', 'strasse', 'PLZ', 'ort',
                  'tel_nr', 'facharzttitel', 'GLN_nr', 'ZSR_nr', 'fachrichtung']
        error_messages = {
            'praxis_name': {
                'unique': 'Ausgewählte Arztpraxis ist bereits registriert'
            },
            'GLN_nr': {
                'unique': 'Diese GLN Nummer ist bereits registriert'
            },
            'ZSR_nr': {
                'unique': 'Diese ZSR Nummer ist bereits registriert'
            },
        }

class CustomPraxisCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Praxis
        fields = ['email', 'password1', 'password2', 'name',  'plz','typ', 'ort']


# form um apotheken zu registrieren
class CustomApothekeCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser

        fields = ['email', 'password1', 'password2', 'vorname', 'nachname',
                  'anrede', 'praxis_name', 'strasse', 'PLZ', 'ort',
                  'tel_nr', 'facharzttitel', 'GLN_nr', 'ZSR_nr', ]
        error_messages = {
            'praxis_name': {
                'unique': 'Ausgewählte Apotheke ist bereits registriert'
            },
            'GLN_nr': {
                'unique': 'Diese GLN Nummer ist bereits registriert'
            },
            'ZSR_nr': {
                'unique': 'Diese ZSR Nummer ist bereits registriert'
            },
        }



class ShippingInfoForm(ModelForm):
    class Meta:
        model = ShippingInfo
        fields = ['email_sender', 'email_receiver',
                  'name_sender', 'name_receiver','address_sender','address_receiver',
                  'city_sender','city_receiver', 'zip_sender',
                  'zip_receiver','state_sender', 'state_receiver',
                  'number_pallets','weight', 'stackable','loading_meters',
                  'cargo_description','dangerous_goods']




class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
