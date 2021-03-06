# Generated by Django 3.1.7 on 2021-05-21 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('vorname', models.CharField(max_length=50)),
                ('nachname', models.CharField(max_length=50)),
                ('fachrichtung', models.CharField(choices=[('Facharzttitel auswählen', 'Facharzttitel auswählen'), ('Allergologie und klinische Immunologie', 'Allergologie und klinische Immunologie'), ('Allgemeine Innere Medizin ', 'Allgemeine Innere Medizin '), ('Angiologie', 'Angiologie'), ('Arbeitsmedizin ', 'Arbeitsmedizin '), ('Chirurgie', 'Chirurgie'), ('Dermatologie und Venerologie', 'Dermatologie und Venerologie'), ('Endokrinologie / Diabetologie ', 'Endokrinologie / Diabetologie '), ('Gastroenterologie ', 'Gastroenterologie '), ('Gynäkologie und Geburtshilfe ', 'Gynäkologie und Geburtshilfe '), ('Hämatologie', 'Hämatologie'), ('Handchirurgie ', 'Handchirurgie '), ('Herz- und thorakale Gefässchirurgie ', 'Herz- und thorakale Gefässchirurgie '), ('Infektiologie ', 'Infektiologie '), ('Intensivmedizin ', 'Intensivmedizin '), ('Kardiologie ', 'Kardiologie '), ('Kinder- und Jugendmedizin ', 'Kinder- und Jugendmedizin '), ('Kinder- und Jugendpsychiatrie und -psychotherapie ', 'Kinder- und Jugendpsychiatrie und -psychotherapie '), ('Kinderchirurgie ', 'Kinderchirurgie '), ('Klinische Pharmakologie und Toxikologie ', 'Klinische Pharmakologie und Toxikologie '), ('Medizinische Genetik ', 'Medizinische Genetik '), ('Medizinische Onkologie ', 'Medizinische Onkologie '), ('Mund-, Kiefer- und Gesichtschirurgie ', 'Mund-, Kiefer- und Gesichtschirurgie '), ('Nephrologie ', 'Nephrologie '), ('Neurochirurgie ', 'Neurochirurgie '), ('Neurologie ', 'Neurologie '), ('Nuklearmedizin ', 'Nuklearmedizin '), ('Ophthalmologie ', 'Ophthalmologie '), ('Orthopädische Chirurgie und Traumatologie des Bewegungsapparates ', 'Orthopädische Chirurgie und Traumatologie des Bewegungsapparates '), ('Oto-Rhino-Laryngologie ', 'Oto-Rhino-Laryngologie '), ('Pathologie ', 'Pathologie '), ('Pharmazeutische Medizin ', 'Pharmazeutische Medizin '), ('Physikalische Medizin und Rehabilitation ', 'Physikalische Medizin und Rehabilitation '), ('Plastische, Rekonstruktive und Ästhetische Chirurgie ', 'Plastische, Rekonstruktive und Ästhetische Chirurgie '), ('Pneumologie', 'Pneumologie'), ('Prävention und Public Health ', 'Prävention und Public Health '), ('Psychiatrie und Psychotherapie ', 'Psychiatrie und Psychotherapie '), ('Radiologie ', 'Radiologie '), ('Radio-Onkologie / Strahlentherapie ', 'Radio-Onkologie / Strahlentherapie '), ('Rheumatologie ', 'Rheumatologie '), ('Rechtsmedizin', 'Rechtsmedizin'), ('Thoraxchirurgie ', 'Thoraxchirurgie '), ('Tropen- und Reisemedizin ', 'Tropen- und Reisemedizin '), ('Urologie ', 'Urologie ')], default='Richtung auswählen', max_length=100)),
                ('anrede', models.CharField(choices=[('Herr', 'Herr'), ('Frau', 'Frau'), ('not_needed', 'not_needed')], max_length=50)),
                ('strasse', models.CharField(max_length=50)),
                ('PLZ', models.IntegerField()),
                ('ort', models.CharField(max_length=50)),
                ('tel_nr', models.CharField(max_length=50)),
                ('facharzttitel', models.CharField(max_length=50)),
                ('GLN_nr', models.IntegerField(unique=True)),
                ('ZSR_nr', models.CharField(max_length=50, unique=True)),
                ('seen_by_praxis', models.BooleanField(default=False)),
                ('accepted_by_praxis', models.BooleanField(default=False)),
                ('sms_auth', models.BooleanField(default=False)),
                ('totp_auth', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_superuser', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Medikament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GTIN', models.IntegerField()),
                ('PRODNO', models.IntegerField()),
                ('DSCRD', models.CharField(max_length=200)),
                ('DSCRF', models.CharField(max_length=200)),
                ('ATC', models.CharField(max_length=200)),
                ('IT', models.CharField(max_length=200)),
                ('PackGrSwissmedic', models.CharField(max_length=200)),
                ('EinheitSwissmedic', models.CharField(max_length=200)),
                ('SubstanceSwissmedic', models.CharField(max_length=400)),
                ('CompositionSwissmedic', models.CharField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='Praxis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('typ', models.CharField(max_length=200)),
                ('plz', models.IntegerField()),
                ('accepted_by_medorg', models.BooleanField(default=True)),
                ('ort', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RezeptMedikamente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rezept', models.IntegerField()),
                ('medikament', models.CharField(max_length=250)),
                ('anzahl_morgen', models.DecimalField(decimal_places=2, max_digits=5)),
                ('anzahl_mittag', models.DecimalField(decimal_places=2, max_digits=5)),
                ('anzahl_abend', models.DecimalField(decimal_places=2, max_digits=5)),
                ('anzahl_nacht', models.DecimalField(decimal_places=2, max_digits=5)),
                ('menge', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bemerkung_medicament', models.CharField(max_length=250)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Rezept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient', models.CharField(max_length=200)),
                ('seen', models.BooleanField(default=False)),
                ('rezept_typ', models.CharField(max_length=50)),
                ('dauer', models.IntegerField()),
                ('del_arzt', models.BooleanField(default=False)),
                ('del_apotheke', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('ref_apotheke_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_apotheke', to='accounts.praxis', to_field='name')),
                ('ref_arzt_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_arzt', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patienteninfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('strasse', models.CharField(max_length=200)),
                ('vorname', models.CharField(max_length=200)),
                ('geburtstag', models.DateField()),
                ('arzt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dazu_arzt', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('ref_apotheke_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apotheke_notif', to=settings.AUTH_USER_MODEL)),
                ('ref_arzt_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='praxis_id', to='accounts.praxis', to_field='name')),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='praxis_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='praxis', to='accounts.praxis', to_field='name'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
