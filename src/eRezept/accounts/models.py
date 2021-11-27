from urllib.parse import urlencode

import requests
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.timezone import datetime
from .managers import CustomUserManager, CustomPraxisManager


anrede_CHOICES = (
    ('Herr','Herr'),
    ('Frau', 'Frau'),
    ('not_needed', 'not_needed')
)

fachrichtung_choices = (
    ('Facharzttitel auswählen','Facharzttitel auswählen'),
    ('Allergologie und klinische Immunologie','Allergologie und klinische Immunologie'),
    ('Allgemeine Innere Medizin ','Allgemeine Innere Medizin '),
('Angiologie','Angiologie'),
('Arbeitsmedizin ','Arbeitsmedizin '),
('Chirurgie','Chirurgie'),
('Dermatologie und Venerologie','Dermatologie und Venerologie'),
('Endokrinologie / Diabetologie ','Endokrinologie / Diabetologie '),
('Gastroenterologie ','Gastroenterologie '),
('Gynäkologie und Geburtshilfe ','Gynäkologie und Geburtshilfe '),
('Hämatologie','Hämatologie'),
('Handchirurgie ','Handchirurgie '),
('Herz- und thorakale Gefässchirurgie ','Herz- und thorakale Gefässchirurgie '),
('Infektiologie ','Infektiologie '),
('Intensivmedizin ','Intensivmedizin '),
('Kardiologie ','Kardiologie '),
('Kinder- und Jugendmedizin ','Kinder- und Jugendmedizin '),
('Kinder- und Jugendpsychiatrie und -psychotherapie ','Kinder- und Jugendpsychiatrie und -psychotherapie '),
('Kinderchirurgie ','Kinderchirurgie '),
('Klinische Pharmakologie und Toxikologie ','Klinische Pharmakologie und Toxikologie '),
('Medizinische Genetik ','Medizinische Genetik '),
('Medizinische Onkologie ','Medizinische Onkologie '),
('Mund-, Kiefer- und Gesichtschirurgie ','Mund-, Kiefer- und Gesichtschirurgie '),
('Nephrologie ','Nephrologie '),
('Neurochirurgie ','Neurochirurgie '),
('Neurologie ','Neurologie '),
('Nuklearmedizin ','Nuklearmedizin '),
('Ophthalmologie ','Ophthalmologie '),
('Orthopädische Chirurgie und Traumatologie des Bewegungsapparates ','Orthopädische Chirurgie und Traumatologie des Bewegungsapparates '),
('Oto-Rhino-Laryngologie ','Oto-Rhino-Laryngologie '),
('Pathologie ','Pathologie '),
('Pharmazeutische Medizin ','Pharmazeutische Medizin '),
('Physikalische Medizin und Rehabilitation ','Physikalische Medizin und Rehabilitation '),
('Plastische, Rekonstruktive und Ästhetische Chirurgie ','Plastische, Rekonstruktive und Ästhetische Chirurgie '),
('Pneumologie','Pneumologie'),
('Prävention und Public Health ','Prävention und Public Health '),
('Psychiatrie und Psychotherapie ','Psychiatrie und Psychotherapie '),
('Radiologie ','Radiologie '),
('Radio-Onkologie / Strahlentherapie ','Radio-Onkologie / Strahlentherapie '),
('Rheumatologie ','Rheumatologie '),
('Rechtsmedizin','Rechtsmedizin'),
('Thoraxchirurgie ','Thoraxchirurgie '),
('Tropen- und Reisemedizin ','Tropen- und Reisemedizin '),
('Urologie ','Urologie '),

)




class Praxis(AbstractBaseUser):
    name = models.CharField(max_length=200, unique=True)
    typ = models.CharField(max_length=200)
    plz = models.IntegerField()
    accepted_by_medorg = models.BooleanField(default=False)
    ort = models.CharField(max_length=200)
    email = models.EmailField(_('email address'), unique=True)


    USERNAME_FIELD = 'email'
    def __str__(self):
        return self.name





class Admin(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)
    is_superuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.email

# Modell für ärzte und apotheken, die unterscheidung erfolgt dann im .views
# file anhand von groups.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    vorname = models.CharField(max_length=50)
    nachname = models.CharField(max_length=50)
    fachrichtung = models.CharField(max_length=100, choices=fachrichtung_choices, default='Richtung auswählen')
    anrede = models.CharField(max_length=50, choices=anrede_CHOICES)
    praxis_name = models.ForeignKey(Praxis, to_field="name", related_name='praxis', on_delete=models.CASCADE)
    strasse = models.CharField(max_length=50)
    PLZ = models.IntegerField()
    ort = models.CharField(max_length=50)
    tel_nr = models.CharField(max_length=50)
    facharzttitel = models.CharField(max_length=50)
    GLN_nr = models.IntegerField(unique=True)
    ZSR_nr = models.CharField(unique=True,max_length=50 )
    seen_by_praxis = models.BooleanField(default=False)
    accepted_by_praxis = models.BooleanField(default=False)
    sms_auth = models.BooleanField(default=False)
    totp_auth = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # aktuell ist unique identifier email, dies muss evt. auf glr nummer gewechselt werden
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email









class shipping_optimized(models.Model):
    id = models.IntegerField(primary_key=True)
    email_sender = models.EmailField(_('email address'), unique=False)
    email_receiver = models.EmailField(_('email address'), unique=False)
    email_zwischenstopp = models.EmailField(_('email address'), unique=False)
    name_sender = models.CharField(max_length=50)
    name_receiver = models.CharField(max_length=50)
    name_zwischenstopp = models.CharField(max_length=50)
    address_sender = models.CharField(max_length=50)
    id_shipping_first = models.IntegerField()
    id_shipping_second = models.IntegerField()
    address_receiver = models.CharField(max_length=50)
    address_zwischenstopp = models.CharField(max_length=50)
    city_sender = models.CharField(max_length=50)
    city_receiver = models.CharField(max_length=50)
    city_zwischenstopp = models.CharField(max_length=50)
    zip_sender = models.IntegerField()
    zip_receiver = models.IntegerField()
    zip_zwischenstopp = models.IntegerField(null=True)
    state_sender = models.CharField(max_length=2)
    state_receiver = models.CharField(max_length=2)
    state_zwischenstopp = models.CharField(max_length=2)
    number_pallets = models.IntegerField()
    loading_meters = models.DecimalField(max_digits=6, decimal_places=3)
    dangerous_goods = models.BooleanField()
    cargo_description = models.CharField(max_length=400)
    weight = models.IntegerField()
    stackable = models.IntegerField()
    date_delivery = models.DateTimeField(default=timezone.now)
    latitude_sender = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, default='0')
    longitude_sender = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, default='0')
    latitude_zwischenstopp = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, default='0')
    longitude_zwischenstopp = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, default='0')
    latitude_receiver = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, default='0')
    longitude_receiver = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, default='0')



    REQUIRED_FIELDS = []


    def __str__(self):
        return str(self.id)

    def save(self, **kwargs):
        self.id = int(f"{self.id_shipping_first}{self.id_shipping_second}")
        data_type = 'json'
        api_key = "AIzaSyB1iop9B4rIjSNxFG4hYAALvF9py2nybew"
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
        address = " ".join(
            [self.address_sender, str(self.zip_sender), self.city_sender])
        params = {"address": address, "key": api_key}
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        r = requests.get(url)

        if r.json()['status'] == 'OK':
            latlng = r.json()['results'][0]['geometry']['location']
            self.latitude_sender = latlng.get("lat")
            self.longitude_sender = latlng.get("lng")
            super().save(**kwargs)
        elif r.json()['status'] == 'ZERO_RESULTS':
            self.latitude_sender = 5.4
            self.longitude_sender = 5.4
            super().save(**kwargs)
        elif r.json()['status'] == 'OVER_DAILY_LIMIT':
            self.latitude_sender = 6.4
            self.longitude_sender = 6.4
            super().save(**kwargs)
        elif r.json()['status'] == 'OVER_QUERY_LIMIT':
            self.latitude_sender = 7.4
            self.longitude_sender = 7.4
            super().save(**kwargs)
        elif r.json()['status'] == 'REQUEST_DENIED':
            self.latitude_sender = 8.4
            self.longitude_sender = 8.4
            super().save(**kwargs)
        elif r.json()['status'] == 'INVALID_REQUEST':
            self.latitude_sender = 9.4
            self.longitude_sender = 9.4
            super().save(**kwargs)
        elif r.json()['status'] == 'UNKNOWN_ERROR':
            self.latitude_sender = 10.4
            self.longitude_sender = 10.4


        address = " ".join(
            [self.address_receiver, str(self.zip_receiver), self.city_receiver])
        params = {"address": address, "key": api_key}
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        r = requests.get(url)

        if r.json()['status'] == 'OK':
            latlng = r.json()['results'][0]['geometry']['location']
            self.latitude_receiver= latlng.get("lat")
            self.longitude_receiver = latlng.get("lng")
            super().save(**kwargs)
        elif r.json()['status'] == 'ZERO_RESULTS':
            self.latitude_receiver = 5.4
            self.longitude_receiver = 5.4
            super().save(**kwargs)
        elif r.json()['status'] == 'OVER_DAILY_LIMIT':
            self.latitude_receiver = 6.4
            self.longitude_receiver = 6.4
            super().save(**kwargs)
        elif r.json()['status'] == 'OVER_QUERY_LIMIT':
            self.latitude_receiver = 7.4
            self.longitude_receiver = 7.4
            super().save(**kwargs)
        elif r.json()['status'] == 'REQUEST_DENIED':
            self.latitude_receiver = 8.4
            self.longitude_receiver = 8.4
            super().save(**kwargs)
        elif r.json()['status'] == 'INVALID_REQUEST':
            self.latitude_receiver = 9.4
            self.longitude_receiver = 9.4
            super().save(**kwargs)
        elif r.json()['status'] == 'UNKNOWN_ERROR':
            self.latitude_receiver = 10.4
            self.longitude_receiver = 10.4

        if (len(self.address_zwischenstopp)):
            address = " ".join(
                [self.address_zwischenstopp, str(self.address_zwischenstopp), self.address_zwischenstopp])
            params = {"address": address, "key": api_key}
            url_params = urlencode(params)
            url = f"{endpoint}?{url_params}"
            r = requests.get(url)

            if r.json()['status'] == 'OK':
                latlng = r.json()['results'][0]['geometry']['location']
                self.latitude_zwischenstopp = latlng.get("lat")
                self.longitude_zwischenstopp = latlng.get("lng")
                super().save(**kwargs)
            elif r.json()['status'] == 'ZERO_RESULTS':
                self.latitude_zwischenstopp = 5.4
                self.longitude_zwischenstopp = 5.4
                super().save(**kwargs)
            elif r.json()['status'] == 'OVER_DAILY_LIMIT':
                self.latitude_zwischenstopp = 6.4
                self.longitude_zwischenstopp = 6.4
                super().save(**kwargs)
            elif r.json()['status'] == 'OVER_QUERY_LIMIT':
                self.latitude_zwischenstopp = 7.4
                self.longitude_zwischenstopp = 7.4
                super().save(**kwargs)
            elif r.json()['status'] == 'REQUEST_DENIED':
                self.latitude_zwischenstopp = 8.4
                self.longitude_zwischenstopp = 8.4
                super().save(**kwargs)
            elif r.json()['status'] == 'INVALID_REQUEST':
                self.latitude_zwischenstopp = 9.4
                self.longitude_zwischenstopp = 9.4
                super().save(**kwargs)
            elif r.json()['status'] == 'UNKNOWN_ERROR':
                self.latitude_zwischenstopp = 10.4
                self.longitude_zwischenstopp = 10.4









class ShippingInfo(models.Model):
    email_sender = models.EmailField(_('email address'), unique=False)
    email_receiver = models.EmailField(_('email address'), unique=False, default='john@example.com', null=True, blank=True)
    name_sender = models.CharField(max_length=50)
    name_receiver = models.CharField(max_length=50, default='John M. Doe', null=True, blank=True)
    address_sender = models.CharField(max_length=50)
    address_receiver = models.CharField(max_length=50, default='542 W. 15th Street', null=True, blank=True)
    city_sender = models.CharField(max_length=50)
    city_receiver = models.CharField(max_length=50, default='New York', null=True, blank=True)
    already_optimized = models.BooleanField(default = False)
    zip_sender = models.IntegerField()
    zip_receiver = models.IntegerField(default=10001, null=True, blank=True)
    state_sender = models.CharField(max_length=2)
    state_receiver = models.CharField(max_length=2, default='NY', null=True, blank=True)
    number_pallets = models.IntegerField(default=120, null=True, blank=True)
    loading_meters = models.DecimalField(max_digits=6, decimal_places=3, default=8.4, null=True, blank=True)
    dangerous_goods = models.BooleanField(default=False, null=True, blank=True)
    cargo_description = models.CharField(max_length=400, blank=True, null=True)
    weight = models.IntegerField(default=1230, null=True, blank=True)
    stackable = models.IntegerField(default=1, null=True, blank=True)
    #TODO replace with this line
    date_delivery = models.DateTimeField(default=timezone.now)
    # deadline = models.DateField(default='2025-12-31')
    latitude_sender = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, default='0')
    longitude_sender = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, default='0')
    latitude_receiver = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, default='0')
    longitude_receiver = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, default='0')
    #TODO add following lines
    # max_truck_height = models.IntegerField()
    # ramp_height = models.IntegerField()
    # from_date = models.DateField(verbose_name='From', null=True, blank=True)
    # until_date = models.DateField(verbose_name='Until', null=True, blank=True)



    REQUIRED_FIELDS = []

    def save(self, **kwargs):
        data_type = 'json'
        api_key = "AIzaSyB1iop9B4rIjSNxFG4hYAALvF9py2nybew"
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
        address = " ".join(
            [self.address_sender, str(self.zip_sender), self.city_sender])
        params = {"address": address, "key": api_key}
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        r = requests.get(url)

        if r.json()['status'] == 'OK':
            latlng = r.json()['results'][0]['geometry']['location']
            self.latitude_sender = latlng.get("lat")
            self.longitude_sender = latlng.get("lng")
            super().save(**kwargs)
        elif r.json()['status'] == 'ZERO_RESULTS':
            self.latitude_sender = 5.4
            self.longitude_sender = 5.4
            super().save(**kwargs)
        elif r.json()['status'] == 'OVER_DAILY_LIMIT':
            self.latitude_sender = 6.4
            self.longitude_sender = 6.4
            super().save(**kwargs)
        elif r.json()['status'] == 'OVER_QUERY_LIMIT':
            self.latitude_sender = 7.4
            self.longitude_sender = 7.4
            super().save(**kwargs)
        elif r.json()['status'] == 'REQUEST_DENIED':
            self.latitude_sender = 8.4
            self.longitude_sender = 8.4
            super().save(**kwargs)
        elif r.json()['status'] == 'INVALID_REQUEST':
            self.latitude_sender = 9.4
            self.longitude_sender = 9.4
            super().save(**kwargs)
        elif r.json()['status'] == 'UNKNOWN_ERROR':
            self.latitude_sender = 10.4
            self.longitude_sender = 10.4


        address = " ".join(
            [self.address_receiver, str(self.zip_receiver), self.city_receiver])
        params = {"address": address, "key": api_key}
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        r = requests.get(url)

        if r.json()['status'] == 'OK':
            latlng = r.json()['results'][0]['geometry']['location']
            self.latitude_receiver= latlng.get("lat")
            self.longitude_receiver = latlng.get("lng")
            super().save(**kwargs)
        elif r.json()['status'] == 'ZERO_RESULTS':
            self.latitude_receiver = 5.4
            self.longitude_receiver = 5.4
            super().save(**kwargs)
        elif r.json()['status'] == 'OVER_DAILY_LIMIT':
            self.latitude_receiver = 6.4
            self.longitude_receiver = 6.4
            super().save(**kwargs)
        elif r.json()['status'] == 'OVER_QUERY_LIMIT':
            self.latitude_receiver = 7.4
            self.longitude_receiver = 7.4
            super().save(**kwargs)
        elif r.json()['status'] == 'REQUEST_DENIED':
            self.latitude_receiver = 8.4
            self.longitude_receiver = 8.4
            super().save(**kwargs)
        elif r.json()['status'] == 'INVALID_REQUEST':
            self.latitude_receiver = 9.4
            self.longitude_receiver = 9.4
            super().save(**kwargs)
        elif r.json()['status'] == 'UNKNOWN_ERROR':
            self.latitude_receiver = 10.4
            self.longitude_receiver = 10.4

    def __str__(self):
        return str(self.id)
